package main

import (
    "encoding/base64"
    "encoding/hex"
    "flag"
    "fmt"
    "io/ioutil"
    "os"
    "regexp"
    "strconv"
    "crypto/hmac"
    "crypto/sha256"
)

func pbkdf2(password, salt []byte, iter, keyLen int) []byte {
    hLen := 32 // sha256
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
    in := flag.String("in", "", "obfuscated go wrapper file")
    out := flag.String("out", "decoded.go", "output file")
    pass := flag.String("pass", "", "password")
    flag.Parse()
    if *in == "" || *pass == "" {
        fmt.Println("Usage: deobfuscator -in wrapper.go -pass password [-out decoded.go]")
        os.Exit(2)
    }
    text, err := ioutil.ReadFile(*in)
    if err != nil {
        fmt.Println("read error:", err)
        os.Exit(1)
    }
    // find base64 payload
    reB64 := regexp.MustCompile("b64 := `([A-Za-z0-9+/=\\n]+)`")
    m := reB64.FindSubmatch(text)
    if m == nil {
        fmt.Println("no payload found")
        os.Exit(3)
    }
    b64 := string(m[1])
    // find salt hex
    reSalt := regexp.MustCompile("saltHex := \"([0-9a-fA-F]+)\"")
    ms := reSalt.FindSubmatch(text)
    if ms == nil {
        fmt.Println("no salt found")
        os.Exit(4)
    }
    salt, _ := hex.DecodeString(string(ms[1]))
    // find iters
    reIters := regexp.MustCompile("iters := (\\d+)")
    mi := reIters.FindSubmatch(text)
    if mi == nil {
        fmt.Println("no iterations found")
        os.Exit(5)
    }
    iters, _ := strconv.Atoi(string(mi[1]))

    raw, _ := base64.StdEncoding.DecodeString(b64)
    key := pbkdf2([]byte(*pass), salt, iters, 32)
    dec := xor(raw, key)
    if err := ioutil.WriteFile(*out, dec, 0644); err != nil {
        fmt.Println("write error:", err)
        os.Exit(6)
    }
    fmt.Println("Wrote decoded file:", *out)
}
