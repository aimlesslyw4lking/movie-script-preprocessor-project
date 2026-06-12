"""Launch implementation"""

import processor as pr
import converter as cv

def main():

    """ 
    Launches implementation (and treats you like a cutie pie)
    """

    print('Hi!! <3    Looking for your scripts now...')
    scripts = pr.find_scripts()
    
    if not scripts:
        raise pr.ScriptNotFoundError("Uh oh... There is no script in the destinated folder...")
        
    print("Scripts found! Let's compile them now <3")
    compiled_scripts = pr.tokenize_and_compile(scripts)
    
    if not compiled_scripts:
        raise pr.ScriptCompilationError("Oops! Something went wrong during the compilation of your script!")
        
    print("Your scripts have been compiled successfully! ^_^ ")
    cleaned_scripts = compiled_scripts

    if not cleaned_scripts:
        raise pr.ScriptPreprocessingError("I'm sorry! Something happened as the scripts were preprocessed..")
        
    print("Yay! The scripts are ready! Let's upload them to a folder now")
    uploaded_scripts = pr.write_cleaned_file(cleaned_scripts)
    
    if not uploaded_scripts:
        raise pr.CleanScriptNotWrittenError("Uh oh! Somethin went wrong while uploading the cleaned script!")
    
    analyzer = pr.UDPipeAnalyzer()

    if not analyzer.process_all():
        raise pr.ScriptPreprocessingError(
        "Failed to generate CoNLL-U files :( )"
        )

    print("CoNLL-U files generated successfully!")
    converter = cv.Converter()
    try:
        converted_files = converter.convert_all()
        print(f"Successfully processed {len(converted_files)} files! (っ˘ω˘ς)")
    except cv.ConverterError as e:
        print(f" (╥﹏╥) Pipeline execution halted due to converter error: {e}")

if __name__ == "__main__":
    main()
