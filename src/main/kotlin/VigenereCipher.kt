import java.io.File
import java.lang.IllegalArgumentException

object VigenereCipher {
    fun encrypted(input: String, key: String, onlyUppercaseLetters: Boolean = false): String {
        if (key.length !in 1..3) throw IllegalArgumentException("Key length incorrect")
        if (key.any { it !in ('A'..'Z') }) throw IllegalArgumentException("Key contains non-uppercase characters")

        val adjustedKey = key.uppercase().repeat(input.length / key.length) + key.substring(0, input.length % key.length)
        return input.uppercase().zip(adjustedKey) { c, k ->
            if (onlyUppercaseLetters && c in 'A'..'Z') (((c - 'A') + (k - 'A')) % 26) + 'A'.code
            else if (c in 'A'..'Z') ((c - 'A') + (k - 'A')) + 'A'.code
            else c.code
        }.map { it.toChar() }.joinToString("")
    }

    fun allSimpleKeys(): List<String> {
        val oneLetterKeys = ('A'..'Z').map { it.toString() }
        val twoLetterKeys = oneLetterKeys.flatMap { a -> oneLetterKeys.map { b -> "$a$b" } }
        val threeLetterKeys = twoLetterKeys.flatMap { a -> oneLetterKeys.map { b -> "$a$b" } }
        return oneLetterKeys + twoLetterKeys + threeLetterKeys
    }

    fun exhaustiveSearchAttack(plainText: String, cipherText: String): List<String> {
        return allSimpleKeys().filter { encrypted(plainText, it, onlyUppercaseLetters = true) == cipherText }
    }
}

fun main(args: Array<String>) {
    val input = args[0]
    val key = args[1]

    // Problem 3
    val cipherText = VigenereCipher.encrypted(input, key, onlyUppercaseLetters = false)
    println("Plain text: $input, Key: $key, Computed cipher text: $cipherText")

    // Problem 4
    val allSimpleKeys = VigenereCipher.allSimpleKeys()
    File("output.txt").printWriter().use { writer ->
        writer.write(allSimpleKeys.size.toString())
        writer.write("\n")
        for (simpleKey in allSimpleKeys) {
            writer.write(simpleKey)
            writer.write("\n")
        }
    }

    val plainText1 = "ARIZONASTATEUNIVERSITY"
    val cipherText1 = "EUCDRHEVNEWYYQCZHLWLNC"
    val keys1 = VigenereCipher.exhaustiveSearchAttack(plainText1, cipherText1)
    println("Plain text: $plainText1, Cipher text: $cipherText1, Found keys: ${keys1.joinToString()}")

    val plainText2 = "COMPUTERSCIENCE"
    val cipherText2 = "GRGTXNIUMGLYRFY"
    val keys2 = VigenereCipher.exhaustiveSearchAttack(plainText2, cipherText2)
    println("Plain text: $plainText2, Cipher text: $cipherText2, Found keys: ${keys2.joinToString()}")

    val commonKeys = keys1.toSet().intersect(keys2.toSet())
    println("Common keys: ${commonKeys.joinToString()}")
}