This folder contains an example pptx template file example-template.pptx. If you want to use your own template files,
you might add a custom class to pptx_template for easier usage (look at the example class TemplateETIT169).
To help you identify shape names etc. in your template, you can use the function analyze_pptx in pptx_template.

Note:
git update-index --assume-unchanged resources/pptx_template/example-template.pptx
revert:
git update-index --no-assume-unchanged resources/pptx_template/example-template.pptx

Use the above commands for your local repository, to prevent unwanted changes to the example template.