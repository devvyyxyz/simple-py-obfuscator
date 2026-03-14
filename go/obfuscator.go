package main

import (
    "crypto/hmac"
    "crypto/rand"
    "crypto/sha256"
    "encoding/base64"
    "encoding/hex"
    "flag"
    "fmt"
    "io"
    "io/ioutil"
    "os"
    "strconv"
)

func pbkdf2(password, salt []byte, iter, keyLen int) []byte {
    hLen := 32 // sha256
    blocks := (keyLen + hLen - 1) / hLen
    dk := make([]byte, 0, blocks*hLen)
    for b := 1; b <= blocks; b++ {
        // U_1 = HMAC(password, salt || INT(b))
        mac := hmac.New(sha256.New, password)
        mac.Write(salt)
        mac.Write([]byte{byte(b >> 24), byte(b >> 16), byte(b >> 8), byte(b)})
        u := mac.Sum(nil)
        t := make([]byte, len(u))
        copy(t, u)
        for i := 1; i < iter; i++ {
            mac = hmac.New(sha256.New, password)
            mac.Write(u)
            u = mac.Sum(nil)
            for j := 0; j < len(t); j++ {
                t[j] ^= u[j]
            }
        }
        dk = append(dk, t...)
    }
    return dk[:keyLen]
}

func xor(data, key []byte) []byte {
    out := make([]byte, len(data))
    for i := range data {
        out[i] = data[i] ^ key[i%len(key)]
    }
    return out
}

func main() {
    in := flag.String("in", "", "input Go file")
    out := flag.String("out", "", "output wrapper file")
    key := flag.String("key", "", "password (optional)")
    flag.Parse()
    if *in == "" || *out == "" {
        fmt.Println("Usage: obfuscator -in input.go -out wrapper.go [-key password]")
        os.Exit(2)
    }

    data, err := ioutil.ReadFile(*in)
    if err != nil {
        fmt.Println("read error:", err)
        os.Exit(1)
    }

    password := *key
    if password == "" {
        fmt.Print("Password: ")
        var b = make([]byte, 128)
        n, _ := os.Stdin.Read(b)
        password = string(b[:n])
        password = string([]byte(password))
        password = password
    }

    salt := make([]byte, 16)
    if _, err := io.ReadFull(rand.Reader, salt); err != nil {
        fmt.Println("salt error:", err)
        os.Exit(1)
    }
    iters := 200000
    keyBytes := pbkdf2([]byte(password), salt, iters, 32)
    enc := xor(data, keyBytes)
    b64 := base64.StdEncoding.EncodeToString(enc)

    // wrapper that decodes and runs the code via `go run`
    wrapper := fmt.Sprintf(`package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"
    "encoding/hex"
    "fmt"
    "io/ioutil"
    "os"
    "os/exec"
)

func pbkdf2(password, salt []byte, iter, keyLen int) []byte {
    hLen := 32
    blocks := (keyLen + hLen - 1) / hLen
    dk := make([]byte, 0, blocks*hLen)
    for b := 1; b <= blocks; b++ {
        mac := hmac.New(sha256.New, password)
        mac.Write(salt)
        mac.Write([]byte{byte(b >> 24), byte(b >> 16), byte(b >> 8), byte(b)})
        u := mac.Sum(nil)
        t := make([]byte, len(u))
        copy(t, u)
        for i := 1; i < iter; i++ {
            mac = hmac.New(sha256.New, password)
            mac.Write(u)
            u = mac.Sum(nil)
            for j := 0; j < len(t); j++ {
                t[j] ^= u[j]
            }
        }
        dk = append(dk, t...)
    }
    return dk[:keyLen]
}

func xor(data, key []byte) []byte {
    out := make([]byte, len(data))
    for i := range data {
        out[i] = data[i] ^ key[i%len(key)]
    }
    return out
}

func main() {
    b64 := `%s`
    saltHex := "%s"
    iters := %d

    pass := os.Getenv("OBF_KEY")
    if pass == "" {
        if len(os.Args) > 1 {
            pass = os.Args[1]
        } else {
            fmt.Print("Password: ")
            var input []byte
            fmt.Scanln(&input)
            pass = string(input)
        }
    }
    salt, _ := hex.DecodeString(saltHex)
    key := pbkdf2([]byte(pass), salt, iters, 32)
    raw, _ := base64.StdEncoding.DecodeString(b64)
    decoded := xor(raw, key)
    tmp := "_decoded.go"
    ioutil.WriteFile(tmp, decoded, 0644)
    cmd := exec.Command("go", "run", tmp)
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.Stdin = os.Stdin
    if err := cmd.Run(); err != nil {
        fmt.Fprintln(os.Stderr, "run error:", err)
        os.Exit(1)
    }
}
`, b64, hex.EncodeToString(salt), iters)

    if err := ioutil.WriteFile(*out, []byte(wrapper), 0644); err != nil {
        fmt.Println("write error:", err)
        os.Exit(1)
    }
    fmt.Println("Wrote Go wrapper:", *out)
}
