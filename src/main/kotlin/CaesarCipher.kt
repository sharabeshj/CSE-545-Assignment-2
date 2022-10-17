object CaesarCipher {
    fun encrypted(input: String, k: Int): String {
        return input.uppercase().map { c ->
            if (c in 'A'..'Z') (((c - 'A') + k) % 26) + 'A'.code
            else c.code
        }.map { it.toChar() }.joinToString("")
    }

    fun statisticalAttack(input: String): List<Pair<Int, String>> {
        val charInput = input.filter { it in 'A'..'Z' }
        val freqMap = charInput.groupBy { it }.mapValues { it.value.size.toDouble() / charInput.length.toDouble() }
        val correlation = (0..25).map { i ->
            ('A'..'Z').sumOf { c ->
                val shifted = if (c.code - i >= 'A'.code) (c.code - i).toChar() else (c.code - i + 26).toChar()
                (freqMap[c] ?: 0.0) * freqOfEnglishChar(shifted)
            }
        }
        val correlationSorted = correlation.withIndex().sortedByDescending { it.value }
        return correlationSorted.map { (i, _) -> Pair(i, encrypted(input, 26 - i)) }
    }

    private fun freqOfEnglishChar(c: Char): Double {
        return mapOf(
                'a' to 0.080, 'b' to 0.015, 'c' to 0.030, 'd' to 0.040, 'e' to 0.130, 'f' to 0.020,
                'g' to 0.015, 'h' to 0.060, 'i' to 0.065, 'j' to 0.005, 'k' to 0.005, 'l' to 0.035,
                'm' to 0.030, 'n' to 0.070, 'o' to 0.080, 'p' to 0.020, 'q' to 0.002, 'r' to 0.065,
                's' to 0.060, 't' to 0.090, 'u' to 0.030, 'v' to 0.010, 'w' to 0.015, 'x' to 0.005,
                'y' to 0.020, 'z' to 0.002
        ).mapKeys { (it.key - 'a' + 'A'.code).toChar() }[c] ?: 0.0
    }
}

fun main(args: Array<String>) {
    // Problem 1
    val input = when (args.size) {
        2 -> args[0]
        else -> ('A'..'Z').joinToString(", ")
    }
    val k = when (args.size) {
        2 -> args[1].toInt()
        1 -> args[0].toInt()
        else -> 3
    }
    val encryptedText = CaesarCipher.encrypted(input, k)
    println("Key: $k, Encrypted text: $encryptedText")

    // Problem 2
    val input1 = "XTKYBFWJXJHZWNYD"
    println("Statistical attack on $input1: ")
    val possibilities = CaesarCipher.statisticalAttack(input1)
    println("Found: Key: ${possibilities.first().first}, plain text: ${possibilities.first().second}")

    val input2 = "KCECMKS"
    println("Statistical attack on $input2: ")
    val possibilities2 = CaesarCipher.statisticalAttack(input2)
    println("Found: Key: ${possibilities2.first().first}, plain text: ${possibilities2.first().second}")
}