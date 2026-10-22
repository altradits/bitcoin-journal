#include "sha256.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

static std::vector<uint8_t> unhex(const std::string& s) {
    std::vector<uint8_t> o;
    for (size_t i = 0; i + 1 < s.size(); i += 2) o.push_back((uint8_t)std::stoi(s.substr(i, 2), nullptr, 16));
    return o;
}
static std::string hex(const std::array<uint8_t, 32>& a) {
    static const char* d = "0123456789abcdef";
    std::string s;
    for (auto b : a) { s += d[b >> 4]; s += d[b & 15]; }
    return s;
}

int main() {
    std::ifstream in("../vectors.tsv");
    if (!in) { std::cerr << "cannot open ../vectors.tsv\n"; return 2; }
    std::string line;
    int bad = 0, n = 0;
    try {
        while (std::getline(in, line)) {
            if (line.empty()) continue;
            std::stringstream ss(line);
            std::string h, a, b;
            std::getline(ss, h, '\t'); std::getline(ss, a, '\t'); std::getline(ss, b, '\t');
            auto d = unhex(h);
            ++n;
            if (hex(sha256(d)) != a) { ++bad; std::cerr << "sha256 mismatch, vector " << n << "\n"; }
            if (hex(sha256d(d)) != b) { ++bad; std::cerr << "sha256d mismatch, vector " << n << "\n"; }
        }
    } catch (const std::exception& e) { std::cerr << "error: " << e.what() << "\n"; return 1; }
    std::cout << (bad ? "FAIL" : "OK") << " (" << n << " vectors)\n";
    return bad ? 1 : 0;
}
