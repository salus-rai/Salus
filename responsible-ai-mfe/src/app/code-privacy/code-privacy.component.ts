/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { environment } from 'src/environments/environment';
import { UserValidationService } from '../services/user-validation.service';
import { NonceService } from '../nonce.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-code-privacy',
  templateUrl: './code-privacy.component.html',
  styleUrls: ['./code-privacy.component.css']
})
export class CodePrivacyComponent {
  form: FormGroup;
  constructor(private _snackBar: MatSnackBar, private cdr: ChangeDetectorRef, public https: HttpClient, private modalservice: NgbModal,private validationService:UserValidationService,public nonceService:NonceService,private sanitizer: DomSanitizer) {
    this.form = new FormGroup({
      file: new FormControl(null, Validators.required)
    });
  }
  demoFile: any[] = [];
  public browseFilesLenth = 0;
  files: any[] = [];
  @ViewChild("fileDropRef", { static: false }) fileDropEl: any = ElementRef;
  showSpinner: any = false;
  public validationLabelDND = "";
  selectedFile: File | any;
  files2: any[] = [];
  textDesc2: any
  textDesc: any
  table = false
  spinner1 = false
  ip_port: any
  privacy_codefile_anonymize = ""
  privacy_code_anonymize = ""
  sampleSrc1 = environment.imagePathurl + '/assets/image/code.png';
  sampleFileFlag = false
  public safeTemplateData!: SafeHtml; 

  ngOnInit(): void {
    // Explainability_Demo
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      if (x != null) {

        this.ip_port = JSON.parse(x)
        console.log("inside parse", this.ip_port.result)
      }
      console.log("ip_port arr v", this.ip_port.result.nemo)
      console.log("ip_port", this.ip_port)
    }

    this.privacy_codefile_anonymize = this.ip_port.result.Privacy + this.ip_port.result.Privacy_codefile_anonymize
    this.privacy_code_anonymize = this.ip_port.result.Privacy + this.ip_port.result.Privacy_code_anonymize
  }

  reset() {
    this.showSpinner = false
    this.spinner1 = false
    this.selectedFile = "";
    this.files = [];
    this.files2 = [];
    this.demoFile = [];
    this.textDesc2 = ""
    this.textDesc = ""
    this.table = false
    this.sampleFileFlag= false;
    this.cdr.detectChanges();

  }

  onButtonClick() {
    this.sampleFileFlag= true;
    this.textDesc = `public class Example {
    // Class-level variable
    private static String name = "John Doe"
    private static String ip = "136.226.232.200"
    private static String email = "johndoe@outlook.com"
    private static String secretkeystring= "cmVnrGtuOjAxOjE3MjEyODUwMjg6M0RrNjVMVGZEaGd6T0RiZ09FR3M5MEV5Tk0z"
    public static void main(String[] args) {
        // Call a method to display the greeting
        displayGreeting(name);
    }
    }`;
  }

  fileBrowseHandler(imgFile: any) {
    console.log("Called")
    this.files = []
    this.demoFile = this.files;
    // to validate file SAST
  const allowedTypes = ['text/plain'];
  for(let i =0; i< this.files.length; i++){
    if (!allowedTypes.includes(this.files[i].type)) {
     alert('Please upload a valid file');
      this.files = [];
      this.demoFile = [];
      return ;
    }
  }
    this.browseFilesLenth = imgFile.target.files.length;
    this.prepareFilesList(imgFile.target.files);
    this.spinner1 = true
    this.uploadDocument(this.demoFile[0])
    this.form.patchValue({ file: this.demoFile[0] });
  }

  uploadDocument(file: any) {
    let fileReader = new FileReader();
    fileReader.onload = (e) => {
      // console.log(fileReader.result);
      this.textDesc = fileReader.result;
      this.spinner1 = false
    }
    fileReader.readAsText(file);
  }

  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      this.files.push(item);
    }
  }
  // uploadcodeFile() {
  //   if (this.files.length == 0) {
  //     this.validationLabelDND = "Please Choose a file to be uploaded in the Table"
  //   } else {
  //     let fileData = new FormData();
  //     const headers = new HttpHeaders({ 'Accept': 'application/octet-stream' });
  //     this.validationLabelDND = "";
  //     for (let i = 0; i < this.demoFile.length; i++) {
  //       this.selectedFile = this.demoFile[i];
  //       fileData.append('code_file', this.selectedFile);
  //       console.log(fileData)
  //     }
  //   }
  // }

  pushToFile(inputText: any) // CODEFILEPUSHING CONVERSION INPUT TO FILE
  {
    const file = new Blob([inputText], { type: 'text/plain' });
    console.log("FILE" + file)
    const fileData = new FormData();
    fileData.append('code_file', file);
    console.log("fileData" + fileData)
    const headers = new HttpHeaders({ 'Accept': 'text/plain' });

    if(this.demoFile.length > 0 || this.sampleFileFlag === true) {
    this.https.post(this.privacy_codefile_anonymize, fileData, { headers, observe: 'response', responseType: 'text' })
      .subscribe((res: any) => {
        this.showSpinner = false

        const fileName = this.extractFileNameFromHeaders(res.headers);
        console.log("file name", fileName)
        console.log("file name", res.body)
        this.textDesc2 = res.body
      }, error => {
        console.log(error)
        const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
        const action = "Close"
        this.showSpinner = false;
        this._snackBar.open(message, action, {
          duration: 3000,
          panelClass: ['le-u-bg-black'],
        });
      })
    } else {
      if (!this.validationService.validateTextDesc(this.textDesc)) {
        console.error('Invalid text description entered');
        this.showSpinner = false;
        // Optionally display an error message to the user
        this._snackBar.open('Invalid characters in text description.', 'Close', {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
        });
        return; // Exit the function if validation fails
    }
      this.https.post(this.privacy_code_anonymize, this.textDesc, { headers, observe: 'response', responseType: 'text' } )
        .subscribe((res: any) => {
          this.showSpinner = false;

          console.log("response body", res.body);
          this.textDesc2 = res.body;
        }, error => {
          console.log(error)
          const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
          const action = "Close"
          this.showSpinner = false;
          this._snackBar.open(message, action, {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
          });
        });
      }
  }
  extractFileNameFromHeaders(headers: HttpHeaders): string {
    const contentDispositionHeader: any = headers.get('content-disposition');
    const matches: any = /filename=([^;]+)/ig.exec(contentDispositionHeader);
    const fileName = (matches[1] || 'untitled').trim();
    return fileName;
  }
  //this.uploadFilesSimulator(0);
  // onUpload() {
  //   this.showSpinner = true
  //   this.uploadcodeFile()
  // }
  onSubmit(inputText: any) {
    this.form.patchValue({ inputText: inputText });
    if (inputText['inputText'] == "" || inputText['inputText'] == null) {
      this._snackBar.open('Please Upload File or Enter Code', '✖', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
      });
      return;
    }
    this.showSpinner = true
    this.pushToFile(inputText['inputText'])
  }
  // Function to sanitize the data before it is used
  sanitizeData(data: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(data);
  }
}