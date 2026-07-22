/**
 * ZERO-KNOWLEDGE VAULT - CRYPTO ENGINE (Giai đoạn 1)
 * 
 * Mô-đun xử lý toàn bộ các thao tác mã hóa / giải mã hoàn toàn ở phía Client (Client-Side Encryption)
 * dựa trên chuẩn Web Crypto API (window.crypto.subtle) của trình duyệt.
 * 
 * Tiêu chuẩn Bảo mật:
 * 1. Key Derivation: PBKDF2-HMAC-SHA-256 (600,000 vòng lặp) -> AES-GCM 256-bit Key.
 * 2. Symmetric Encryption: AES-256-GCM (với IV 96-bit ngẫu nhiên cho mỗi lần mã hóa).
 * 3. Non-Extractable Key: Khóa CryptoKey không thể bị export ra ngoài RAM dưới dạng thô (extractable = false).
 * 4. Raw Storage: Server chỉ nhận Encrypted Blob (Base64), Salt (Base64), và IV (Base64).
 */

export interface EncryptedVaultPayload {
  /** Chuỗi mã hóa (Base64) */
  ciphertext: string;
  /** Vector khởi tạo (Base64, 12 bytes) */
  iv: string;
  /** Muối ngẫu nhiên (Base64, 32 bytes) dùng để dérivé khóa */
  salt: string;
}

export class CryptoService {
  /** Số vòng lặp PBKDF2 theo khuyến nghị OWASP (tối thiểu 600,000) */
  private static readonly PBKDF2_ITERATIONS = 600_000;
  /** Độ dài Salt (32 bytes = 256 bits) */
  private static readonly SALT_BYTE_LENGTH = 32;
  /** Độ dài IV khuyến nghị cho AES-GCM (12 bytes = 96 bits) */
  private static readonly IV_BYTE_LENGTH = 12;

  // ==========================================
  // HELPER FUNCTIONS (Base64 <-> ArrayBuffer)
  // ==========================================

  /**
   * Chuyển đổi từ ArrayBuffer / Uint8Array sang chuỗi Base64
   */
  public static bufferToBase64(buffer: ArrayBuffer | Uint8Array): string {
    const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    let binary = "";
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  /**
   * Chuyển đổi từ chuỗi Base64 sang Uint8Array
   */
  public static base64ToBuffer(base64: string): Uint8Array {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  }

  // ==========================================
  // CORE CRYPTO ENGINE APIs
  // ==========================================

  /**
   * 1. Tạo Salt ngẫu nhiên bảo mật cao bằng Web Crypto API
   * @param length Độ dài salt tính bằng byte (mặc định 32 bytes)
   * @returns Uint8Array chứa các byte ngẫu nhiên
   */
  public static generateSalt(length: number = CryptoService.SALT_BYTE_LENGTH): Uint8Array {
    const salt = new Uint8Array(length);
    crypto.getRandomValues(salt);
    return salt;
  }

  /**
   * 2. Dẫn xuất AES-256 Key từ Master Password và Salt sử dụng PBKDF2 (SHA-256, 600,000 vòng)
   * 
   * Quyền truy cập khóa: extractable = false (không thể trích xuất khóa thô ra ngoài RAM).
   * 
   * @param masterPassword Mật khẩu Master của người dùng
   * @param salt Salt ngẫu nhiên (Uint8Array hoặc Base64 string)
   * @returns Promise<CryptoKey> Khóa AES-GCM 256-bit trong bộ nhớ RAM
   */
  public static async deriveKey(
    masterPassword: string,
    salt: Uint8Array | string
  ): Promise<CryptoKey> {
    if (!masterPassword || masterPassword.trim().length === 0) {
      throw new Error("Master Password không được để trống.");
    }

    const saltBuffer = typeof salt === "string" ? CryptoService.base64ToBuffer(salt) : salt;
    const encoder = new TextEncoder();

    // Bước A: Import chuỗi Master Password thành Key Material ban đầu cho PBKDF2
    const keyMaterial = await crypto.subtle.importKey(
      "raw",
      encoder.encode(masterPassword),
      { name: "PBKDF2" },
      false, // Không cho phép trích xuất key material
      ["deriveKey"]
    );

    // Bước B: Chạy PBKDF2 với HMAC-SHA-256 (600,000 vòng) để tạo khóa AES-GCM 256-bit
    const derivedKey = await crypto.subtle.deriveKey(
      {
        name: "PBKDF2",
        salt: saltBuffer,
        iterations: CryptoService.PBKDF2_ITERATIONS,
        hash: "SHA-256",
      },
      keyMaterial,
      {
        name: "AES-GCM",
        length: 256, // AES-256
      },
      false, // BẢO MẬT: extractable = false (không xuất được AES Key thô)
      ["encrypt", "decrypt"]
    );

    return derivedKey;
  }

  /**
   * 3. Mã hóa dữ liệu JSON Vault bằng AES-256-GCM
   * 
   * Mỗi lần mã hóa sẽ tự động sinh một IV (Initialization Vector) 96-bit mới.
   * 
   * @param dataJson Chuỗi JSON chứa danh sách tài khoản / mật khẩu
   * @param key Khóa AES-GCM đã được deriveKey() tạo ra
   * @returns Promise<{ ciphertext: string, iv: string }> Trả về Ciphertext (Base64) và IV (Base64)
   */
  public static async encryptVault(
    dataJson: string,
    key: CryptoKey
  ): Promise<{ ciphertext: string; iv: string }> {
    // Tạo IV ngẫu nhiên 12-byte (96-bit) cho chuẩn AES-GCM
    const iv = new Uint8Array(CryptoService.IV_BYTE_LENGTH);
    crypto.getRandomValues(iv);

    const encoder = new TextEncoder();
    const encodedData = encoder.encode(dataJson);

    // Mã hóa bằng AES-GCM (Web Crypto API tự động gắn Authentication Tag vào cuối Ciphertext)
    const encryptedBuffer = await crypto.subtle.encrypt(
      {
        name: "AES-GCM",
        iv: iv,
      },
      key,
      encodedData
    );

    return {
      ciphertext: CryptoService.bufferToBase64(encryptedBuffer),
      iv: CryptoService.bufferToBase64(iv),
    };
  }

  /**
   * 4. Giải mã Ciphertext về lại chuỗi JSON Vault ban đầu
   * 
   * Nếu sai Master Password (dẫn tới sai Key) hoặc dữ liệu bị chỉnh sửa (Authentication Tag thất bại),
   * Web Crypto API sẽ tự động văng lỗi OperationError.
   * 
   * @param ciphertextBase64 Chuỗi mã hóa Base64
   * @param key Khóa AES-GCM
   * @param ivBase64 Vector IV Base64
   * @returns Promise<string> Chuỗi JSON ban đầu
   */
  public static async decryptVault(
    ciphertextBase64: string,
    key: CryptoKey,
    ivBase64: string
  ): Promise<string> {
    const ciphertextBuffer = CryptoService.base64ToBuffer(ciphertextBase64);
    const ivBuffer = CryptoService.base64ToBuffer(ivBase64);

    try {
      const decryptedBuffer = await crypto.subtle.decrypt(
        {
          name: "AES-GCM",
          iv: ivBuffer,
        },
        key,
        ciphertextBuffer
      );

      const decoder = new TextDecoder();
      return decoder.decode(decryptedBuffer);
    } catch (error) {
      throw new Error(
        "Giải mã thất bại! Master Password không chính xác hoặc dữ liệu đã bị chỉnh sửa/can thiệp."
      );
    }
  }
}
