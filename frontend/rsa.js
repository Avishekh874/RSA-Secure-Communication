
// ============================================
// RSA KEY GENERATION MODULE
// Algorithm: RSA-OAEP
// Key Size: 2048 bits
// Hash: SHA-256
// ============================================

window.RSA = (() => {

    let publicKey = null;
    let privateKey = null;
    let publicKeyBase64 = null;

    // Convert ArrayBuffer into Base64
    function arrayBufferToBase64(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = "";

        for (const byte of bytes) {
            binary += String.fromCharCode(byte);
        }

        return btoa(binary);
    }

    // Generate RSA public and private key pair
    async function generateKeyPair() {

        try {
            console.log("Starting RSA-2048 key generation...");

            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "RSA-OAEP",
                    modulusLength: 2048,
                    publicExponent: new Uint8Array([1, 0, 1]),
                    hash: "SHA-256"
                },
                false,
                ["encrypt", "decrypt"]
            );

            publicKey = keyPair.publicKey;
            privateKey = keyPair.privateKey;

            // Export only the public key
            const exportedPublicKey =
                await window.crypto.subtle.exportKey(
                    "spki",
                    publicKey
                );

            publicKeyBase64 =
                arrayBufferToBase64(exportedPublicKey);

            console.log("RSA key pair generated successfully!");
            console.log("Algorithm: RSA-OAEP");
            console.log("Key size: 2048 bits");
            console.log("Hash: SHA-256");
            console.log("Public key format: Base64-encoded SPKI");
            console.log("Public key:", publicKeyBase64);
            console.log("Private key: Stored in browser memory only.");
            console.log("Private key exportable:", privateKey.extractable);

            return {
                success: true,
                publicKey: publicKeyBase64
            };

        } catch (error) {
            console.error("RSA key generation failed:", error);
            throw error;
        }
    }

    // Return the generated public key
    function getPublicKey() {
        return publicKeyBase64;
    }

    // Check whether keys have been generated
    function isKeyPairGenerated() {
        return publicKey !== null && privateKey !== null;
    }

    // Expose only the required functions
    return {
        generateKeyPair,
        getPublicKey,
        isKeyPairGenerated
    };

})();
