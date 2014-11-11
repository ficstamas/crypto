#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# decrypto
# Copyright 2014 Christopher Simpkins
# MIT license
#------------------------------------------------------------------------------

# Application start
def main():
    import sys
    import getpass
    from Naked.commandline import Command
    from Naked.toolshed.shell import muterun
    #from Naked.toolshed.state import StateObject
    from Naked.toolshed.system import dir_exists, directory, filename, file_exists, list_all_files, make_path, stdout, stderr

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------
    # [ Instantiate state object ]
    #------------------------------------------------------------------------------
    # state = StateObject()
    #------------------------------------------------------------------------------------------
    # [ VALIDATION LOGIC ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    #------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from crypto.settings import usage as crypto_usage
        print(crypto_usage)
        sys.exit(1)
    #------------------------------------------------------------------------------------------
    # [ HELP, VERSION, USAGE LOGIC ]
    # Naked framework provides default help, usage, and version commands for all applications
    #   --> settings for user messages are assigned in the lib/crypto/settings.py file
    #------------------------------------------------------------------------------------------
    if c.help():      # User requested crypto help information
        from crypto.settings import help as crypto_help
        print(crypto_help)
        sys.exit(0)
    elif c.usage():   # User requested crypto usage information
        from crypto.settings import usage as crypto_usage
        print(crypto_usage)
        sys.exit(0)
    elif c.version(): # User requested crypto version information
        from crypto.settings import app_name, major_version, minor_version, patch_version
        version_display_string = app_name + ' ' + major_version + '.' + minor_version + '.' + patch_version
        print(version_display_string)
        sys.exit(0)
    #------------------------------------------------------------------------------------------
    # [ APPLICATION LOGIC ]
    #
    #------------------------------------------------------------------------------------------
    elif c.argc > 1:
    # code for multi-file processing and commands that include options
        stdout("multi")

    elif c.argc == 1:
    # simple single file or directory processing with default settings
        path = c.arg0
        if file_exists(path):
            check_existing_file = False # check for a file with the name of new decrypted filename in the directory

            if path.endswith('.crypt'):
                new_filename = path[0:-6] # remove the .crypt suffix
                check_existing_file = True
            elif path.endswith('.gpg') or path.endswith('.pgp') or path.endswith('.asc'):
                new_filename = path[0:-4]
                check_existing_file = True
            else:
                new_filename = path + ".decrypt" #if there is not a standard file type, then add a .decrypt suffix to the decrypted file name
                stdout("Could not confirm that the requested file is encrypted based upon the file type.  Attempting decryption.  Keep your fingers crossed...")

            # confirm that the decrypted path does not already exist, if so abort with warning message to user
            if check_existing_file == True:
                if file_exists(new_filename):
                    stderr("Your file will be decrypted to '" + new_filename + "' and this file path already exists.  Please move the file or use the --overwrite option with your command if you intend to replace the current file.")
                    sys.exit(1)

            # get passphrase used to symmetrically encrypt the file
            passphrase = getpass.getpass("Please enter your passphrase: ")
            passphrase_confirm = getpass.getpass("Please enter your passphrase again: ")

            # confirm that the passphrases match
            if passphrase == passphrase_confirm:
                system_command = "gpg --batch -o " + new_filename + " --passphrase " + passphrase + " -d " + path

                response = muterun(system_command)
                # overwrite user entered passphrases
                passphrase = ""
                passphrase_confirm = ""

                if response.exitcode == 0:
                    stdout("Decryption complete")
                    sys.exit(0)
                else:
                    stderr(response.stderr, 0)
                    stderr("Decryption failed")
                    sys.exit(1)

        elif dir_exists(path):
            pass # TODO add decryption code - keep this explicit suffix requirement

    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        print("Could not complete your request.  Please try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
