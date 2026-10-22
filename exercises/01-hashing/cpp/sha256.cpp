#include "sha256.hpp"
#include <stdexcept>

// Implement FIPS 180-4 yourself.
std::array<uint8_t, 32> sha256(const std::vector<uint8_t>& data) {
    (void)data;
    throw std::logic_error("not implemented");
}

std::array<uint8_t, 32> sha256d(const std::vector<uint8_t>& data) {
    auto a = sha256(data);
    return sha256(std::vector<uint8_t>(a.begin(), a.end()));
}
