# Unit 19: Multi Blockchain Wallet in Python by John Mangahas

## Dependencies
----

The following dependencies are required for this assignment;

1. HD Wallet Derive
2. `bit` Python Bitcoin Library
2. `web3.py` Python Ethereum Library

## Project Setup
----

1. Create a project directory called `unit19` and `cd` into it using gitbash (Run as Administrator).

2. Clone the `hd-wallet-derive` tool into this folder 

![setup](images/hd-wallet1.png)

![setup](images/hd-wallet2.png)

3. Establish a symlink called derive for the `hd-wallet-derive/hd-wallet-derive.php`. This will clean up the command needed to run the script in our code, as we can call ./derive instead of ./hd-wallet-derive/hd-wallet-derive.php.

![setup](images/hd-wallet3.png)

4. Make sure you are in the top level project directory - in this case the directory named `unit19`.

5. Run the command `export MSYS=winsymlinks:nativestrict`.

6. Run the following command: `ln -s hd-wallet-derive/hd-wallet-derive.php derive`.

7. Test the `./derive` script, by running the following command:

`php hd-wallet-derive.php -g --mnemonic="mnemonic phrase of your test wallet" --cols=path,address,privkey,pubkey`

8. The output will be several addresses corresponding privkey and pubkey

![setup](images/hd-wallet4.png)