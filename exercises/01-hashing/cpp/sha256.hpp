#pragma once
#include <array>
#include <cstdint>
#include <vector>

std::array<uint8_t, 32> sha256(const std::vector<uint8_t>& data);
std::array<uint8_t, 32> sha256d(const std::vector<uint8_t>& data);
