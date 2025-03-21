/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { TemplateBasedGuardrailService } from '../../request-moderation/template-based-guardrail/template-based-guardrail.service';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { RightSidePopupComponent } from '../../right-side-popup/right-side-popup.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-template-based-guardrail-response',
  templateUrl: './template-based-guardrail-response.component.html',
  styleUrls: ['./template-based-guardrail-response.component.css']
})
export class TemplateBasedGuardrailResponseComponent implements OnChanges {
  @Input() llmEvalPayload: any;
  @Input() responseModerationTemplates:any;
  @Input() selectedUseCaseName: any;
  @Input() setLoadTemplateResMod:Boolean = false;
  @Input() templateBasedPayload: any;
  textareaContext = '';
  naviResponse :any = {};
  response: any = {}

  status: any = {}

  constructor(private dialog: MatDialog,private templateBasedService: TemplateBasedGuardrailService,private sharedDataService: SharedDataService) { 
    this.sharedDataService.naviToneModerationRes.subscribe(response => {
      this.naviResponse = response
    });
  }
  ngOnInit() {
    this.templateBasedService.fetchApiUrl()
  }
  ngOnChanges(changes: SimpleChanges) {
    console.log("Template Based Guardrail Response Component", changes)
    if (changes['setLoadTemplateResMod'] && changes['setLoadTemplateResMod'].currentValue === true) {
      console.log("Template Based Guardrail Response Component @TEMPLATEBASED");
      this.callBatch();
    }
  }
  async callBatch() {
    this.responseModerationTemplates.forEach((element: any) => {
      this.status[element] = '';
      this.response[element] = {};
    });
    const batchSize = 3; 
    for (let i = 0; i < this.responseModerationTemplates.length; i += batchSize) {
      const batchPromises = [];
      for (let j = i; j < i + batchSize && j < this.responseModerationTemplates.length; j++) {
        const templatesToIgnore = ['RESPONSE_COMPLETENESS_WRT_CONTEXT'];
        if (!templatesToIgnore.includes(this.responseModerationTemplates[j])){
          batchPromises.push(this.callEvalLLM(this.responseModerationTemplates[j]));
        }
      }
      await Promise.all(batchPromises).then(results => {
        console.log('Batch completed', results);
      }).catch(error => {
      });
    }
    console.log('All requests processed');
  }

  isEmptyObject(obj: any): boolean {
    return obj != null && typeof obj === 'object' && Object.keys(obj).length === 0;
  }

 

  callEvalLLM(templateName: any, Context?: any): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.status[templateName] === 'loading' || this.status[templateName] === 'done') {
        if ((templateName == 'RESPONSE_COMPLETENESS_WRT_CONTEXT' && this.status[templateName] === 'done')) {
          this.response[templateName] = {}
        } else {
          reject('Operation already in progress or completed');
          return;
        }
      }
      this.status[templateName] = 'loading';
      let payload = {
        Prompt: this.llmEvalPayload.Prompt,
        template_name: templateName,
        model_name: this.llmEvalPayload.model_name,
        AccountName: this.templateBasedPayload?.AccountName ? this.templateBasedPayload?.AccountName : "None",
        "PortfolioName": this.templateBasedPayload?.PortfolioName ? this.templateBasedPayload?.PortfolioName : "None",
        "userid": this.templateBasedPayload?.userid,
        "lotNumber": 1,
        // "Context": Context ? Context : "None",
        // "Concise_Context": "None",
        // "Reranked_Context": "None",
        "temperature": this.llmEvalPayload.temperature,
        "PromptTemplate": this.llmEvalPayload.PromptTemplate,
      };
      console.log(payload);
      this.templateBasedService.evalLLM(payload).subscribe(
        (res: any) => {
          if(typeof res?.['moderationResults'] != 'object'){
            this.status[templateName] = 'failed';
            reject("Error in response from evalLLM");
            return 
          }
          this.response[templateName] = res?.['moderationResults'];
          this.response[templateName]['description'] = res?.['description'];
          this.response[templateName]['timetaken'] = res?.['timeTaken'];
          let data = {
            'analysis': this.response[templateName].analysis,
            'result': this.response[templateName].result,
          };
          let templateToIgnore = ['Response Conciseness Check','Response Completeness Check','Response Language Critique Grammar Check'];
          if (data.result === 'FAILED' && !templateToIgnore.includes(templateName)){ 
            this.sharedDataService.updateResponses(templateName, data);
          }
          // if (data.result === 'FAILED'){
          //   this.sharedDataService.updateResponses(templateName, data);
          // }
          this.status[templateName] = 'done';
          console.log(this.response);
          resolve(data); // Resolve the promise with the data
        },
        error => {
          this.status[templateName] = 'failed';
          console.log(error);
          reject(error); // Reject the promise with the error
        }
      );
    });
  }

  openRightSideModal(data: any) {
    const dialogRef = this.dialog.open(RightSidePopupComponent, {
      width: '52vw',
      data: data,
      backdropClass: 'custom-backdrop'
    });
  }


  showFullAnalysis: { [key: string]: boolean } = {
  };

  toggleAnalysis(template: string): void {
    this.showFullAnalysis[template] = !this.showFullAnalysis[template];
  }
  shouldTrim(template: string): boolean {
    const regex = /^Response/;
    return regex.test(template);
  }
}