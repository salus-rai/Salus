/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, INJECTOR, Input } from '@angular/core';
import { RightSidePopupComponent } from '../right-side-popup/right-side-popup.component';
import { MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ResponseComparisonService } from './response-comparison.service';
import { SharedDataService } from 'src/app/services/shared-data.service';
import { AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { Node, Edge } from '@swimlane/ngx-graph';
import { KeyValue } from '@angular/common';
import { urlList } from 'src/app/urlList';
import Chart from 'chart.js/auto';
@Component({
  selector: 'app-response-comparison',
  templateUrl: './response-comparison.component.html',
  styleUrls: ['./response-comparison.component.css']
})
export class ResponseComparisonComponent {
  @Input() openAIRes: any;
  @Input() cotState: any;
  @Input() thotState: any;
  @Input() fmRes: any;
  @Input() covState: any;
  @Input() nemoModerationRailRes: any;
  @Input() prompt: any;
  @Input() tokenImpState: any;
  @Input() gotState: any;
  @Input() hallucinationSwitchCheck: boolean = false;
  @Input() hallucinateRetrievalKeplerRes: any;
  @Input() RagMultiModalResponse: any;
  @Input() gEvalres: any;
  @Input() serperResponseState: any;
  @Input() selectedUseCaseName: any;
  @Input() llmExplainState: any;
  @Input() templateBasedPayload:any;
  @Input() submitFlag:any;
  @Input() selectedTranslate:any;
  imageFailedCases:any = {};
  covResponse: any = {}
  cotResponse: any = {}
  thotResponse: any = {}
  tokenImportanceResponse: any = {};
  activeTab = 'Faithfulness Check';
  apiEndpoints: any = {};
  ApiCallHappened = new Set<string>();
  isSerperSelected: any = false;
  responseSerper: any = {};
  responseSerperStatus = '';
  UncertaintyAIMetric:any;
  refLink: any = '';
  model_name = 'gpt4';
  templateBasedResponse: any = {}
  naviResponse: any = {};
  graphData: any = [];
  chart: any;
  apiResult: any = {};
  nodes: Node[] = [];
  links: Edge[] = [];
  isLoading: boolean = false;
  responseBlocked: boolean = false;
  openAIResTextFormatted: any = '';
  generatedTextFormatted = '';
  GOTExpanded = false;
  llmExplainResponse: any = {};
  isArrowDown: boolean = true;
  metrics = ['uncertainty', 'coherence'];
  UncertaintyGotMetric:any;
  UncertaintyCotMetric:any;
  selectCoveComplexity: any = 'simple';
  selectedLlmModel: any = 'gpt4';
  summary:boolean = true;
  topTokens: any[] = [];
  tokens:any[] = [];
  GOTAnswer: string = '';
  enableSearch = urlList.enableInternetSearch;
  isCollapsed = false
  constructor(private dialog: MatDialog, private responseService: ResponseComparisonService, public _snackBar: MatSnackBar, private https: HttpClient, private cdr: ChangeDetectorRef, private sharedDataService: SharedDataService) {
    this.sharedDataService.templateBasedResponses.subscribe(response => {
      this.templateBasedResponse = response
      console.log(this.templateBasedResponse,"templateBased Service Data")
    });
    this.sharedDataService.imageBasedFailedChecks.subscribe(response => {
      this.imageFailedCases = response
      console.log(this.imageFailedCases.modelBased,this.imageFailedCases.templateBased,"imageFailedCases Service Data")
    });
    this.sharedDataService.naviToneModerationRes.subscribe(response => {
      this.naviResponse = response
      console.log(this.naviResponse)
    });
  }
  ngOnInit(): void {
    this.responseService.fetchApiUrl();
    this.model_name = this.serperResponseState.model;
    if (this.submitFlag && !this.hallucinationSwitchCheck) {
      this.covgetApi();
    }
    console.log("covState.payload", this.covState.payload)
    console.log("submitFlag",this.submitFlag)
    //this.generatedTextFormatted = this.formatText(this.fmRes?.moderationResults?.responseModeration?.generatedText);
    this.RagMultiModalResponse.response.text = this.RagMultiModalResponse?.response?.text?.replace(/\n\n/g, '<br>');
  }
  toggleCollapse() {
    this.isCollapsed = !this.isCollapsed;
}

isTHOTCollapsed = false;
  isGOTCollapsed = false;
    isTokenCollapsed = false;
isCOTCollapsed = false;
 
    toggleTHOTCollapse() {
        this.isTHOTCollapsed = !this.isTHOTCollapsed;
    }
   toggleGOTCollapse() {
        this.isGOTCollapsed = !this.isGOTCollapsed;
    }
 
    toggleCOTCollapse() {
        this.isCOTCollapsed = !this.isCOTCollapsed;
    }
toggleTokenCollapse(): void {
      this.isTokenCollapsed = !this.isTokenCollapsed;
    }


  formatText(text: any) {
    if (!text) {
      return '';
    }
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
  }

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  changeTab = (tab: string) => {
    this.activeTab = tab;
  }

  isEmptyObject(obj: any) {
    if (obj == null || obj == undefined) {
      return true;
    }
    return Object.keys(obj).length === 0;
  }
  
  toggleArrow() {
    this.isArrowDown = !this.isArrowDown;
  }

  openSource(baseResUrl: any) {
    var binaryPdf = atob(baseResUrl);
    var blobPdf = new Blob([new Uint8Array(Array.from(binaryPdf).map(c => c.charCodeAt(0)))], { type: 'application/pdf' });
    var pdfUrl = URL.createObjectURL(blobPdf);
    window.open(pdfUrl, '_blank');
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['le-u-bg-black'],
    });
  }

  isNonEmptyArray(value: any): boolean {
    return Array.isArray(value) && value.length > 0;
  }

  openRightSideModal(data: any) {
    const dialogRef = this.dialog.open(RightSidePopupComponent, {
      width: '52vw',
      data: data,
      backdropClass: 'custom-backdrop'
    });
  }

  covgetApi() {
    if (this.ApiCallHappened.has('covgetApi')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-Cov-get-api-already-called");
      return;
    }
    this.covState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-covGet-API-CALL", this.covState);
    this.ApiCallHappened.add('covgetApi');
    let apiObservable;
    if (this.covState.hallucination) {
      console.log("HALLUCINATION COV")
      apiObservable = this.responseService.hallucinateCOV(this.covState.payload);
    } else {
      const payload1 = {
        "text": this.prompt,
        "complexity": this.selectCoveComplexity,
        "model_name": this.selectedLlmModel,
        "translate": this.selectedTranslate
      }
      apiObservable = this.responseService.covgetApi(payload1);
    }

    apiObservable.subscribe(
      (res: any) => {
        console.log(res)
        if (this.covState.hallucination) {
          this.covResponse.baseline = res.cov_response.baseline_response.replace(/\n/g, '<br>');
          this.covResponse.verification = res.cov_response.verification_answers.replace(/\n/g, '<br>');
          this.covResponse.final = res.cov_response.final_answer.replace(/\n/g, '<br>');
        } else {
          this.covResponse.baseline = res.baseline_response.replace(/\n/g, '<br>');
          let formattedText = res.verification_answers
          .replace(/Question: 1/, 'Question: 1')
          .replace(/Question: 2/, '<br><br>Question: 2')
          .replace(/Question: 3/, '<br><br>Question: 3')
          .replace(/Question: 4/, '<br><br>Question: 4')
          .replace(/Question: 5/, '<br><br>Question: 5')
          .replace(/Answer:/g, '<br>Answer:');
          this.covResponse.verification = formattedText;
          this.covResponse.final = res.final_answer.replace(/\n/g, '<br>');
          this.generatedTextFormatted= res.final_answer.replace(/\n/g, '<br>');
        }
        this.covResponse.timetaken = res.timetaken;
      },
      error => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-COV-API", error);
        this.covState.status = 'FAILED'
        this.ApiCallHappened.delete('covgetApi');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in COV API";
        }
        this.openSnackBar(message, "Close")
      }
    );
    // this.responseService.covgetApi(this.covState.payload).subscribe(
    //   (res: any) => {
    //     this.covResponse.baseline = res.baseline_response.replace(/\n/g, '<br>');
    //     this.covResponse.verification = res.verification_answers.replace(/\n/g, '<br>');
    //     this.covResponse.final = res.final_answer.replace(/\n/g, '<br>');
    //     this.covResponse.timetaken = res.timetaken;
    //   },
    //   error => {
    //     console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-covgetApi", error);
    //     this.covState.status == 'FAILED'
    //     this.ApiCallHappened.delete('covgetApi');
    //     this.openSnackBar("Error in COV API", "Close")
    //   }
    // );
  }

  callCOT() {
    if (this.ApiCallHappened.has('openAicotgetApi')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-openAicotgetApi-already-called");
      return;
    }
    this.cotState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-openAicotgetApi-CALL", this.cotState);
    this.ApiCallHappened.add('openAicotgetApi');

    let apiObservable;
    if (this.cotState.hallucination) {
      apiObservable = this.responseService.hallucinateCOT(this.cotState.payload);
    } else {
      apiObservable = this.responseService.openAicotgetApi(this.cotState.payload);
    }

    apiObservable.subscribe(
      (res: any) => {
        if (this.cotState.hallucination) {
          this.cotResponse.text = res.cot_response.replace(/\n/g, '<br>').split('Source:')[0];
          this.cotResponse.sourceText = res['source-name'];
          this.cotResponse.token_cost = res['token_cost']
        } else {
          this.cotResponse.text = res.text.replace(/\n/g, '<br>');
          const payload1 = {
            "inputPrompt": this.llmExplainState.payload['inputPrompt'],
            "response": this.cotResponse.text
          }
          console.log("payload1:", payload1)
          this.responseService.llmExplain(payload1).subscribe((res: any) => {
            this.UncertaintyCotMetric = res;
          },
            error => {
              console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-llmExplain", error);
              this.llmExplainState.status = 'FAILED'
              this.ApiCallHappened.delete('llmExplain');
              let message
              if (error.status === 500) {
                message = "Internal Server Error. Please try again later.";
              } else {
                message = error.error.detail || error.error.message || "Error in LLM Explain   API";
              }
              this.openSnackBar(message, "Close")
            })
        }
        this.cotResponse.timetaken = res.timetaken;
        console.log(this.cotResponse)
      }
      ,
      error => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-openAicotgetApi", error);
        this.cotState.status = 'FAILED'
        this.ApiCallHappened.delete('openAicotgetApi');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in openAicotgetApi";
        }
        this.openSnackBar(message, "Close")
      }
    );
  }
  callTHOT() {
    if (this.ApiCallHappened.has('openAiTHOTApi')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-openAiTHOTApi-already-called");
      return;
    }
    this.thotState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-openAiTHOTApi-CALL", this.thotState);
    this.ApiCallHappened.add('openAiTHOTApi');

    let apiObservable;
    if (this.thotState.hallucination) {
      apiObservable = this.responseService.hallucinateThot(this.thotState.payload);
    } else {
      apiObservable = this.responseService.openAiTHOTApi(this.thotState.payload);
    }

    apiObservable.subscribe(
      (res: any) => {
        if (this.thotState.hallucination) {
          this.thotResponse.thot_response = res.thot_response.replace(/\n/g, '<br>').split('Source:')[0];
          this.thotResponse.sourceText = res['source-name']
          this.thotResponse.token_cost = res['token_cost']
        } else {
          //this.thotResponse.thot_response = res.text.replace(/\n/g, '<br>');
            let formattedText = res.text
            .replace(/Result:/g, '<br>')
            .replace(/Explanation:/g, '<br>')
            .replace(/\n\n/g, '<br>')
            .replace(/\n/g, '<br>');
            this.thotResponse.thot_response = formattedText;

            const lines = res?.text?.split('\n');
            const resultLine = lines.find((line: any) => line.startsWith('Result:'));
            const explanationLine = lines.find((line: any) => line.startsWith('Explanation:'));

            console.log("Lines::",formattedText)
          
            let resultValue = '';
            let explanationValue = '';
          
            // if (resultLine) {
            //   resultValue = resultLine.split('Result:')[1]?.replace(/"/g, ''); // Remove the surrounding quotes
            // }      
            // if (explanationLine) {
            //   explanationValue = explanationLine.split('Explanation:')[1]?.replace(/"/g, ''); // Remove the surrounding quotes
            // }
            // if (resultLine) {
            //   resultValue = resultLine.split('Result:')[1] // Trim leading and trailing whitespace
            //   const nextNewLineIndex = resultValue.indexOf('\n');
            //   if (nextNewLineIndex !== -1) {
            //     resultValue = resultValue.substring(0, nextNewLineIndex).trim();
            //   }
            // }
            
            // if (explanationLine) {
            //   explanationValue = explanationLine.split('Explanation:')[1]?.trim(); // Trim leading and trailing whitespace
            //   const nextNewLineIndex = explanationValue.indexOf('\n');
            //   if (nextNewLineIndex !== -1) {
            //     explanationValue = explanationValue.substring(0, nextNewLineIndex);
            //   }
            // }
            // if(!resultLine || !explanationLine){
            //   this.thotResponse.thot_response = formattedText;
            // } else {        
            // this.thotResponse.thot_response = `${resultValue}<br>${explanationValue}`;
            // }
            
            const payload1 = {
              "inputPrompt": this.llmExplainState.payload['inputPrompt'],
              "response": this.thotResponse.thot_response
            }
            console.log("payload1:", payload1)
            this.responseService.llmExplain(payload1).subscribe((res: any) => {
              this.UncertaintyAIMetric = res;
            },
              error => {
                console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-llmExplain", error);
                this.llmExplainState.status = 'FAILED'
                this.ApiCallHappened.delete('llmExplain');
                let message
                if (error.status === 500) {
                  message = "Internal Server Error. Please try again later.";
                } else {
                  message = error.error.detail || error.error.message || "Error in LLM Explain   API";
                }
                this.openSnackBar(message, "Close")
              })
        }
        this.thotResponse.timetaken = res.timetaken;
      },
      error => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-openAiTHOTApi", error);
        this.thotState.status = 'FAILED'
        this.ApiCallHappened.delete('openAiTHOTApi');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in Open Ai THOT Api";
        }
        this.openSnackBar(message, "Close")
      }
    );

    // this.responseService.openAiTHOTApi(this.thotState.payload).subscribe(
    //   (res: any) => {
    //     this.thotResponse.timetaken = res.timetaken;
    //     this.thotResponse.thot_response = res.text.replace(/\n/g, '<br>');
    //   },
    //   error => {
    //     console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-openAiTHOTApi", error);
    //     this.thotState.status = 'FAILED'
    //     this.ApiCallHappened.delete('openAiTHOTApi');
    //     this.openSnackBar("Error in openAiTHOTApi", "Close")
    //   }
    // );
  }

  tokenImportance() {
    if (this.ApiCallHappened.has('tokenImportance')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-tokenImportance-already-called");
      return;
    }
    this.tokenImpState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-tokenImportance-CALL", this.tokenImpState);
    this.ApiCallHappened.add('tokenImportance');
 
    this.responseService.tokenImportance(this.tokenImpState.payload).subscribe(
      (res: any) => {
        this.tokenImportanceResponse = res;
        this.tokens = res?.token_importance_mapping;
        console.log("Tokens populated:", this.tokens);
        this.updatetopTokens();
        console.log("Top tokens updated:", this.topTokens);
        this.createTokenBarChart();
        console.log("Token bar chart created");
       
        // this.createFrequencyBarChart();
        this.frequencyDistributionChart();
        console.log("Frequency distribution chart created");
      },
      error => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-tokenImportance", error);
        this.tokenImpState.status = 'FAILED'
        this.ApiCallHappened.delete('tokenImportance');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in token Importance API";
        }
        this.openSnackBar(message, "Close")
      }
    );
  }
  toggleSearch(event: any) {
    this.isSerperSelected = event.target.checked;
    console.log("search:::", this.isSerperSelected);
    if (this.isSerperSelected) {
      this.responseSerper = {};
      // this.refLink ='';
      // call llm-explain api
      this.serperResponseState.payload['llm_response'] = this.fmRes?.moderationResults?.responseModeration?.generatedText;
      this.responseService.serperResponse(this.serperResponseState.payload).subscribe((res: any) => {
        this.responseSerper = res.metrics[0];
        this.generatedTextFormatted=res.internetResponse[0];
        // this.refLink = res.referenxceLink;
      }, (error) => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-serperResponse", error);
        this.responseSerperStatus = 'FAILED'
      }
      )
    }
    else{
      this.generatedTextFormatted=this.formatText(this.fmRes?.moderationResults?.responseModeration?.generatedText);
    }
  }

  getGOT() {
    if (this.ApiCallHappened.has('got')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-got-already-called");
      return;
    }
    this.gotState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-got-CALL", this.gotState);
    this.ApiCallHappened.add('got');
    this.responseService.gotResponse(this.gotState.payload).subscribe(
      (res: any) => {
        this.apiResult = res;
        this.GOTAnswer = res.final_thought.replace(/\n/g, '<br>');
        //this.updateGraph();
        const payload1 = {
          "inputPrompt": this.llmExplainState.payload['inputPrompt'],
          "response": res.final_thought
        }
        console.log("payload1:", payload1)
        this.responseService.llmExplain(payload1).subscribe((res: any) => {
          this.UncertaintyGotMetric = res;
        },
          error => {
            console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-llmExplain", error);
            this.llmExplainState.status = 'FAILED'
            this.ApiCallHappened.delete('llmExplain');
            let message
            if (error.status === 500) {
              message = "Internal Server Error. Please try again later.";
            } else {
              message = error.error.detail || error.error.message || "Error in LLM Explain   API";
            }
            this.openSnackBar(message, "Close")
          })
      },
      error => {
        this.gotState.status = 'FAILED'
        this.ApiCallHappened.delete('got');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in token Importance API";
        }
        this.openSnackBar(message, "Close")
      }
    );
  }

  updateGraph() {
    console.log('updateGraph called');
    this.nodes = [];
    this.links = [];
    console.log('apiResult.graph:', this.apiResult.graph);
    this.apiResult.graph.forEach((graph: any, index: number) => {
      if (graph.operation) {
        const operationId = `operation${index}`;
        this.nodes.push({ id: operationId, label: `Operation: ${graph.operation}`, data: { color: '#ffbbff' } });

        console.log('operation:', graph.operation);

        graph.thoughts.forEach((thought: any, thoughtIndex: number) => {
          if (thought.current) {
            const thoughtId = `${operationId}thought${thoughtIndex}`;
            const thoughtLabel = `${thought.current}, Score: ${thought.score}`;
            this.nodes.push({ id: thoughtId, label: thoughtLabel });
            this.links.push({ id: `link${operationId}${thoughtId}`, source: operationId, target: thoughtId, label: 'Thought' });

            console.log('thought:', thoughtLabel);
          }
        });
      }
    });
    this.isLoading = false;
    console.log('nodes:', this.nodes);
    console.log('links:', this.links);
    this.cdr.detectChanges();
  }
  llmExplanation() {
    if (this.ApiCallHappened.has('llmExplain')) {
      console.log("--RESPONSIBLE-COMPARISON-|||-llmExplain-already-called");
      return;
    }
    this.llmExplainState.status = 'inPROCESS'
    console.log("--RESPONSIBLE-COMPARISON-|||-llmExplain-CALL", this.llmExplainState);
    this.ApiCallHappened.add('llmExplain');
    const payload = {
      "inputPrompt": this.llmExplainState.payload['inputPrompt'],
      "response": this.fmRes?.moderationResults?.responseModeration?.generatedText
    }
    console.log("payload:", payload)
    this.responseService.llmExplain(payload).subscribe((res: any) => {
      this.llmExplainResponse = res;
      //this.UncertaintyAIMetric = res;
    },
      error => {
        console.log("--RESPONSIBLE-COMPARISON-|||-Error-in-llmExplain", error);
        this.llmExplainState.status = 'FAILED'
        this.ApiCallHappened.delete('llmExplain');
        let message
        if (error.status === 500) {
          message = "Internal Server Error. Please try again later.";
        } else {
          message = error.error.detail || error.error.message || "Error in LLM Explain   API";
        }
        this.openSnackBar(message, "Close")
      })
  }
  get llmExplainResponseArray(): Array<KeyValue<string, any>> {
    return Object.entries(this.llmExplainResponse).map(([key, value]) => ({ key, value }));
  }
  updatetopTokens() {
    this.topTokens = this.tokens
      .sort((a: any, b: any) => b.importance_score - a.importance_score);
      this.topTokens = this.topTokens.slice(0, 10);
      (console.log('topTokens:', this.topTokens));
}
 ngAfterViewChecked(): void {
    if (this.isTokenCollapsed && this.tokens.length > 0) {
      this.createTokenBarChart();
      this.frequencyDistributionChart();
 
    }
  }
  createTokenBarChart(): void {
    if (!this.tokens || this.tokens.length === 0) {
        console.log("No tokens available to create the chart.");
        return;
    }
 
    const ctx = document.getElementById('myTokenBarChart1') as HTMLCanvasElement;
    if (!ctx) {
        console.error("Canvas element not found.");
        return;
    }
 
    console.log("Creating token bar chart with tokens:", this.tokens);
 
    // Extracting tokens and importance scores from tokens
    const labels = this.tokens.map(token => token.token);
    const data = this.tokens.map(token => token.importance_value);
 
    const backgroundColorPlugin = {
        beforeDraw: (chart: Chart) => {
            const ctx = chart.canvas.getContext('2d');
            if (ctx) {
                const chartArea = chart.chartArea;
                ctx.save();
                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = '#c1d1f1a0';
                ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                ctx.restore();
            }
        }
    };
 
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tokens',
                data: data,
                backgroundColor: '#2ca02c',
                borderColor: '#2ca02c',
                borderWidth: 1
            }]
        },
        options: {
          plugins: {
            legend: {
              display: true,
              position: 'top', // You can adjust position as per your preference (top, bottom, left, right)
          labels: {
          generateLabels: function(chart) {
          return [{
            text: 'Tokens', // Custom label for green bars
            fillStyle: '#2ca02c', // Color of the bars (green)
            strokeStyle: '#2ca02c', // Border color (green)
          }];
        }
      }
          }
          },
        scales: {
          x: {
            grid: {
              display: false
            },
            title: {
              display: true,
              text: 'Tokens'
          }
          },
          y: {
            grid: {
              //display: false
            },
            beginAtZero: true,
            min: 0,
            max: 1,
            ticks: {
              stepSize: 0.2
            },
            title: {
              display: true,
              text: 'Importance Score'
          }
          }
        }
      }
    });
  }
  frequencyDistributionChart(): void {
    if (!this.tokens || this.tokens.length === 0) {
        console.log("No tokens available to create the chart.");
        return;
    }
 
    const ctx = document.getElementById('myDistributionBarChart1') as HTMLCanvasElement;
    if (!ctx) {
        console.error("Canvas element not found.");
        return;
    }
 
    console.log("Creating frequency distribution chart with tokens:", this.tokens);
 
    // Group frequencies into specified ranges, starting with '0'
    const ranges = ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'];
    const rangeCounts = { '0': 0, '0.1': 0, '0.2': 0, '0.3': 0, '0.4': 0, '0.5': 0, '0.6': 0, '0.7': 0, '0.8': 0, '0.9': 0, '1.0': 0 };
 
    this.tokens.forEach((token: any) => {
      const value = token.importance_value;
      if (value === 0) {
          rangeCounts['0']++;
      } else if (value > 0 && value < 0.1) {
          rangeCounts['0.1']++;
      } else if (value >= 0.1 && value < 0.2) {
          rangeCounts['0.2']++;
      } else if (value >= 0.2 && value < 0.3) {
          rangeCounts['0.3']++;
      } else if (value >= 0.3 && value < 0.4) {
          rangeCounts['0.4']++;
      } else if (value >= 0.4 && value < 0.5) {
          rangeCounts['0.5']++;
      } else if (value >= 0.5 && value < 0.6) {
          rangeCounts['0.6']++;
      } else if (value >= 0.6 && value < 0.7) {
          rangeCounts['0.7']++;
      } else if (value >= 0.7 && value < 0.8) {
          rangeCounts['0.8']++;
      } else if (value >= 0.8 && value < 0.9) {
          rangeCounts['0.9']++;
      } else if (value >= 0.9 && value <= 1.0) {
          rangeCounts['1.0']++;
      }
    });
 
    const data = Object.values(rangeCounts) as number[];
 
    new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ranges,
          datasets: [
              {
                  label: 'Distribution of Importance Scores',
                  data: data,
                  backgroundColor: '#1f77b4',
                  borderColor: '#1f77b4',
                  borderWidth: 1,
                  order: 2 // This dataset is behind the line
              },
              {
                  label: 'Frequency Line',
                  data: data,
                  type: 'line',
                  borderColor: 'red',
                  borderWidth: 2,
                  fill: false,
                  pointRadius: 0,
                  tension: 0.4,
                  order: 1 // This dataset is in front of the bars
              }
          ]
      },
      options: {
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                generateLabels: function(chart) {
                  return [
                    {
                      text: 'Distribution of Importance Scores', // Custom label for blue
                      fillStyle: '#1f77b4', // Color of the bar (blue)
                      strokeStyle: '#1f77b4', // Border color (blue)
                    },
                    {
                      text: 'Frequency Line', // Custom label for red line
                      fillStyle: 'red', // Color of the line (red)
                      strokeStyle: 'red', // Border color (red)
                    }
                  ];
                }
              }
          }
          },
          scales: {
              x: {
                  grid: {
                      display: false
                  },
                  title: {
                      display: true,
                      text: 'Importance Score Range'
                  }
              },
              y: {
                  beginAtZero: true,
                  min: 0,
                  title: {
                      display: true,
                      text: 'Frequency'
                  },
                  ticks: {
                      stepSize: 1
                  }
              }
          }
      }
    });
  }
}
