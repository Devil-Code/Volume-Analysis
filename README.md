# Volume Analysis Tool

This repository contains a Python tool for analyzing the Master Boot Record (MBR) of a disk image. The tool extracts partition information, checks for consistency, and identifies unpartitioned disk space.

## Features

- **Parse MBR**: Extracts partition entries from the Master Boot Record (MBR).
- **Consistency Check**: Verifies the consistency of partitions based on their Logical Block Addressing (LBA) and size.
- **Unpartitioned Space**: Identifies and reports unpartitioned disk space.
- **Partition Details**: Provides detailed information about each partition including CHS address, LBA, size, and type.

## Requirements

- Python 3.x
- NumPy
- Tabulate

## Usage

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Devil-Code/Volume-Analysis-Tool.git
    cd volume-analysis-tool
    ```

2. **Install the required packages**:
    ```bash
    pip install numpy tabulate
    ```

3. **Run the tool**:
    ```bash
    python volume_analysis.py <disk_image>
    ```

    Replace `<disk_image>` with the path to your disk image file.

## Functions

#### `parse_mbr(disk_file)`

Parses the MBR of the given disk image file and extracts partition information.

### `unpartitioned_space()`

Identifies and reports unpartitioned disk space.

### `check_lba_consistency(disk_file)`

Checks the consistency of partitions based on their LBA and size.

### `consistency_check(partition)`

Verifies the consistency of a given partition.

### `output_func(MBR)`

Prints the partition information in a tabulated format.

### `partition_calc(partition)`

Calculates and returns detailed information about a given partition.

### `partition_type(partition)`

Returns the type of a given partition.

### `lba(partition)`

Extracts and returns the LBA of a given partition.

### `size_calc(partition)`

Calculates and returns the size of a given partition in MB.

### `validity_check(partition)`

Checks the validity of a given partition.

### `CHS_calc(partition)`

Calculates and returns the CHS address of a given partition.

### `bintodec(li)`

Converts a binary list to a decimal number.

### `hextodec(li)`

Converts a hexadecimal list to a decimal number.

## Example

```bash
python volume_analysis.py disk_image.dd
```

This will output the partition information and unpartitioned space for the given disk image.

## License

This project is licensed under the GNU GPL v3.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any inquiries or issues, please contact:
- **Pritesh Gandhi**
- **Email**: pgandhi1412@gmail.com
- **GitHub**: [YourGitHubProfile](https://github.com/Devil-Code)

For questions or suggestions, please open an issue in this repository.
