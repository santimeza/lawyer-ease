"# lawyer-ease"

InputObject {
--title:
--id: (a reference symbol that will be in the JSON pdf to denote this specific input object)
--componentType: (html form type)
----optional: (ex. fields in drop down)
--schema: (ex. zod date, social security # -- input validation)
--description: (html text to be displayed)
--error: (html text for input error)
}

Diff algo:

- process pdf -> convert to some sort of txt
- tokenize by words
- group into sentances. Sentances that dont match will be processed in the next step
- process sentances

algo (file1, file2):
--f1 = processFile(file1)
--f2 = processFile(file2)

--tf1, tf2 = tokenize(f1, f2) //tokenize files by sentances
--processedFileDif = [("", bool)] // list of tuples, each containing the full sentance and match or no match (from dif algo)
--processedFileDif = sentenceDiff(tf1, tf2)
--finalForm = noMatchFixer(processedFileDif)

noMatchFixer(file):
--tokenized each no match sentance by word
--run compare algo we drew out to find start and end points of each match no match segment
--replace no match segments with a unique symbol
--// for later, no match recognition of input field and a table to convert input fields to symbols
--return processed file

--// final form will spit out the single processedFileObject with symbols where the no match's were
