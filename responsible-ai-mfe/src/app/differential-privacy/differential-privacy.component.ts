/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.
"
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"
*/ 
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FileHandler } from './fileHandler'
import { Helper } from './helper';
import { DifferentialPrivacyService } from './differential-privacy.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormBuilder, FormGroup, FormArray, FormControl, Validators } from '@angular/forms';
import { NonceService } from '../nonce.service';

@Component({
  selector: 'app-differential-privacy',
  templateUrl: './differential-privacy.component.html',
  styleUrls: ['./differential-privacy.component.css'],
  // encapsulation: ViewEncapsulation.None
})
export class DifferentialPrivacyComponent implements OnInit {
  supressionList: any;
  noiseList=[];
  rangeList=[];
  binaryList=[];

  constructor(private differentialPrivacyService: DifferentialPrivacyService, public _snackBar: MatSnackBar,private fb: FormBuilder,public nonceService:NonceService) 
  { 
    this.fromCreation()
    this.fileHandler = new FileHandler();
  }


  form!: FormGroup;


  showSpinner1 = false;
  showSpinner2 = false;
  showSpinner3 = false;
  fileHandler = new FileHandler();
  helper = new Helper();



  options = [
    { label: 'Option 1', value: '1' },
    { label: 'Option 2', value: '2' },
    { label: 'Option 3', value: '3' },
    { label: 'Option 4', value: '4' },
  ];
  selectedOptions: string[] = [];
  intialFromstatus= false

  ngOnInit(): void {
    let ip_port: any

    let user = this.helper.getLogedInUser()

    ip_port = this.helper.getLocalStoreApi()
    this.helper.setApilist(ip_port)
    // this.fromCreation()
  }
  isLoading = false;
  submit() {
    // this.isLoading=true;
    const allowedTypes = ['text/csv'];
    for(let i =0; i< this.fileHandler.file.length; i++){
      if (!allowedTypes.includes(this.fileHandler.file.type)) {
        this._snackBar.open('Please upload valid file', 'Close', {
          duration: 2000,
        });
       this.fileHandler.reset();
        return ;
      }
    }
    if (this.fileHandler.fileExitsValidator() ==true) {
      this.postFile()
    }
  }

  // Uploads the selected file to the server and processes the response to populate dropdown options.
  postFile() {
    this.showSpinner1 = true;
    let formData = new FormData();
    formData.append('dataset', this.fileHandler.file);
    
    this.differentialPrivacyService.postData(this.helper.diff_priv_file, formData).subscribe((res: any) => {
      console.log("res", res)
      this.setSelectOptionsList(res)
      
      this.showSpinner1 = false;
      this.intialFromstatus = true;
      this._snackBar.open('File uploaded successfully', 'Close', {
        duration: 2000,
      });
    }
    ,error=>{
      this.errormessageCall(error)
    }
  );
  }
  setSelectOptionsList(res: any){
    this.supressionList = res.allHeadders
      this.noiseList = res.numaricHeadder
      this.rangeList = res.numaricHeadder
      this.binaryList = res.binaryHeadder
  }

  fromCreation(){
    this.form = new FormGroup({
      supressionList: new FormControl([],Validators.required),
      noiseList: new FormControl([],Validators.required),
      rangeList: new FormControl([],Validators.required),
      binaryList: new FormControl([],Validators.required),
    });
  }
  
// Submits the form data to the server for anonymization and triggers a file download upon success.
  submitFrom(){
    if (this.form.valid) {
    console.log("form",this.form.value)
    this.showSpinner2 = true;
    const fileData = new FormData();
    fileData.append('suppression', this.form.value.supressionList);
    fileData.append('noiselist', this.form.value.noiseList);
    fileData.append('rangeList', this.form.value.rangeList);
    fileData.append('binarylist', this.form.value.binaryList);
    this.differentialPrivacyService.postform(this.helper.diff_priv_anonymize, fileData).subscribe((data: any) =>
       {
        this.showSpinner2 = false;
        const blob = new Blob([data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'data.csv';
        link.click();
        window.URL.revokeObjectURL(url);
    }
    ,error=>{
      this.errormessageCall(error)
    });
  }else{
    this._snackBar.open('Please select all the options', 'Close', {
      duration: 2000,
    });
  }
  }

  // 
  reset() {
    // Reset form controls
    this.form.reset({
      supressionList: [],
      noiseList: [],
      rangeList: [],
      binaryList: [],
    });
  
    // Reset variables
    this.showSpinner1 = false;
    this.showSpinner2 = false;
    this.showSpinner3 = false;
    this.intialFromstatus = false;
    this.selectedOptions = [];
    // this.fileHandler = new FileHandler(); // Assuming FileHandler is a class with a constructor that initializes its state
    this.fileHandler.reset();
  
    // Reset lists
    this.supressionList = null;
    this.noiseList = [];
    this.rangeList = [];
    this.binaryList = [];
  
    // Close any open snack bars
    this._snackBar.dismiss();
  }

  // Displays an error message in a snackbar for API failures.
  errormessageCall(error: any){
      // const message = error.error.detail
      const message = (error && error.error && (error.error.detail || error.error.message)) || "The Api has failed"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
          });
    
  }
  
}