class Converter():

    def get_binary(self, hex_data):
        # Quick and dirty way to calculate bin from hex
        binary = bin(int('1' + hex_data, 16))[3:]
        return binary

    def separator(self, data_to_separate):
        # Returning list of separated HEX items
        separated_data = [data_to_separate[i:i + 2] for i in range(0, len(data_to_separate), 2)]
        return separated_data

    def converter_from_hex(self, hex_data):
        # Converting from HEX to Bin
        print(hex_data)
        parts_len = int(len(hex_data) / 2)
        parts = self.separator(hex_data)
        converted_bin = []
        for part in parts:
            converted = self.get_binary(part)
            converted_bin.append(converted)
        self.converter_to_hex(converted_bin)
        return converted_bin

    def get_hex(self, bin_data):
        # Quick and dirty way to calculate HEX from BIN
        bin_str = bin_data.replace(' ', '')
        hex_str = '%0*X' % ((len(bin_str) + 3) // 4, int(bin_str, 2))
        return hex_str

    def converter_to_hex(self, binary_data):
        # Converting from Bin to HEX
        final_hex = ''
        for binary in binary_data:
            small_hex = self.get_hex(binary)
            final_hex = final_hex + small_hex
        print(final_hex)
        return final_hex


convert = Converter()
convert.converter_from_hex('00ED6E7220211CE090')
