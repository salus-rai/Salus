/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, Input, OnInit, AfterViewInit  } from '@angular/core';
import { Chart } from  'chart.js/auto';;
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { RightSidePopupComponent } from '../right-side-popup/right-side-popup.component';
import { urlList } from 'src/app/urlList';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';


@Component({
  selector: 'app-explainability-result',
  templateUrl: './explainability-result.component.html',
  styleUrls: ['./explainability-result.component.css']
})
export class ExplainabilityResultComponent implements OnInit, AfterViewInit  {
  @Input() explainabilityRes: any;
  @Input() explainabilityOption!: string;
  @Input() prompt!: string;
  @Input() ExplanabilityFileId!: any;
  @Input() selectedOptions: any;
  @Input() selectedTranslate: any;
  @Input() covFinalAnswer:any;
  @Input() finalAnswer:any;
  @Input() COVAnswer: any;
  @Input() isLoadingCOV: any;
  topSentiments: any[] = [];
  apiResult: any = null;
  //finalAnswer: string = '';
  finalAnswer1: string = '';
  openAIAnswer: string = '';
  THOTAnswer: string = '';
  UncertaintyGotMetric:any;
  UncertaintyAIMetric:any;
   // COVAnswer: string = '';
  GOTAnswer: string = '';
  tokenImportanceResponse: any = {};
  InternetSearchMetric: any  ;
  InternetResponse:any ;
  COVRAGResponse: string = '';
  THOTRAGResponse: string = '';
  THOTRAGSource: any;
  RetrivalKelperResponse: any = {};
  ThotRagResult:any ='';
  ThotRagExplanation:any ='';
  //covFinalAnswer:any;
  //isLoadingCOV: boolean = false;
  isLoadingOpenAI: boolean = false;
  isLoadingTHOT: boolean = false;
  isLoadingUncertainty: boolean = false;
  isLoadingGOT: boolean = false;
  isLoadingTokenImportance: boolean = false;
  isLoadingSearch: boolean = false;
  isSerperSelected: boolean = false;
  isLoadingCOVRAG: boolean = false;
  isLoadingTHOTRAG: boolean = false;
  isLoadingRetrivalKelper: boolean = false;
  isArrowDown: boolean = true;
  option= '';
  enableSearch = urlList.enableInternetSearch;
  private COVUrl:any;
  private OpenAIUrl :any;
  private THOTUrl:any;
  private UncertaintyUrl:any;
  private GOTUrl :any;
  private TokenUrl :any;
  private InternetUrl :any;
  private COVRAGUrl :any;
  private THOTRAGUrl :any;
  explApiUrl :any;
  metrics = ['uncertainty', 'coherence'];
  tokenImage1!: SafeUrl;
  tokenImage2!: SafeUrl;
  topTokens: any[] = [];
  tokens:any[] = [];
  tokenImportanceShowErrorMessage: boolean = false;
  firstClick= true;
  constructor(private https: HttpClient, private dialog: MatDialog,private sanitizer: DomSanitizer) {}

  ngOnInit() {
    this.option= this.explainabilityOption;
    let ip_port: any;
    ip_port = this.getLocalStoreApi();
    // seting up api list
    this.setApilist(ip_port);


    console.log("fgn::",this.explainabilityOption)
    console.log("selectedOption",this.selectedOptions)
    if (this.selectedOptions['Explainability']) {
   if(this.explainabilityOption == 'LLM'){
      //this.COV();
    this.OpenAI();
    //this.THOT();
    this.GOT();
    // this.TokenImportance();
    }else if (this.explainabilityOption == 'RAG') {
     this.COVRAG();
     this.THOTRAG();
    }
  }
  //this.updateTopSentiments();
  this.topSentiments = this.explainabilityRes?.explanation?.[0]?.token_importance_mapping
  // this.createBarChart();
  }
  
  getLocalStoreApi() {
    let ip_port;
    if (localStorage.getItem('res') != null) {
      const x = localStorage.getItem('res');
      if (x != null) {
        return (ip_port = JSON.parse(x));
      }
    }
  }
  setApilist(ip_port: any) {
     this.COVUrl = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_COV;
  this.OpenAIUrl = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openai;
 this.THOTUrl = ip_port.result.FM_Moderation + ip_port.result.OpenAiThot;
  this.UncertaintyUrl = ip_port.result.Llm_Explain + ip_port.result.Uncertainty;
 this.GOTUrl =  ip_port.result.Llm_Explain + ip_port.result.ExplainGOT;;
  this.TokenUrl = ip_port.result.Llm_Explain + ip_port.result.Token_Importance;
  this.InternetUrl = ip_port.result.Llm_Explain + ip_port.result.SerperResponse;
  this.COVRAGUrl =  ip_port.result.Rag + ip_port.result.RagCOV;
  this.THOTRAGUrl = ip_port.result.Rag + ip_port.result.RagTHOT;
  this.explApiUrl = ip_port.result.Explainability;
  }
  callLocalExplain(){
    this.https.post(this.explApiUrl, { inputText: prompt, "explainerID": 1 }).subscribe((expRes) => {
      this.explainabilityRes = expRes
      console.log(expRes)
    }, error => {
    })
  }
  ngAfterViewInit(): void {
    // this.createBarChart();
    if(this.explainabilityOption == 'Sentiment'){this.createBarChart();}
    this.TokenImportance();
  }
  createBarChart(): void {
    const ctx = document.getElementById('myBarChart') as HTMLCanvasElement;

    // Extracting tokens and importance scores from topSentiments
    const labels = this.topSentiments?.map(sentiment => sentiment.token);
    const data = this.topSentiments?.map(sentiment => sentiment.importance_score / 100);
    const backgroundColorPlugin = {
      id: 'customCanvasBackgroundColor',
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
          borderColor:'#2ca02c',
          borderWidth: 1
        }]
      },
      options: {
        // layout: {
        //   backgroundColor: 'rgba(240, 240, 240, 0.5)' 
        // },
        scales: {
          x: {
            grid: {
              display: false
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
            }
          }
        }
      },
      plugins: [backgroundColorPlugin]
    });
  }
  // updateTopSentiments() {
  //   if (this.explainabilityRes?.explanation?.length > 0) {
  //     this.topSentiments = this.explainabilityRes.explanation[0].token_importance_mapping
  //       .sort((a: any, b: any) => b.importance_score - a.importance_score);
  //       this.topSentiments = this.topSentiments.slice(0, 10);
  //       (console.log('topSentiments:', this.topSentiments));
  //   }
  // }
  openRightSideModal(data: any) {
    const dialogRef = this.dialog.open(RightSidePopupComponent, {
      width: '52vw',
      data: data,
      backdropClass: 'custom-backdrop'
    });
  }
  toggleArrow() {
    this.isArrowDown = !this.isArrowDown;
    if(this.firstClick===true){
    // this.TokenImportance();
     }
    this.firstClick= false;
  }

  // COV() {
  //   this.isLoadingCOV = true;
  //   const payload = {
  //     complexity: 'simple',
  //     model_name: 'gpt4',
  //     translate: this.selectedTranslate,
  //     text: this.prompt
  //   };

  //   this.https.post(this.COVUrl, payload)
  //     .subscribe((response: any) => {
  //       console.log('API response:', response);
  //       this.covFinalAnswer = response.final_answer;
  //       this.finalAnswer = this.covFinalAnswer;
  //       let formattedText = response.verification_answers
  //       .replace(/Question: 1/, 'Question: 1')
  //       .replace(/Question: 2/, '<br><br>Question: 2')
  //       .replace(/Question: 3/, '<br><br>Question: 3')
  //       .replace(/Question: 4/, '<br><br>Question: 4')
  //       .replace(/Question: 5/, '<br><br>Question: 5')
  //       .replace(/Answer:/g, '<br>Answer:');
  //       this.COVAnswer = formattedText;
  //       this.isLoadingCOV = false;
  //     }, error => {
  //       this.isLoadingCOV = false;
  //     });
  // }

  OpenAI() {
    this.isLoadingOpenAI = true;
    const payload1 = {
      temperature: '0',
      model_name: 'gpt4',
      Prompt: this.prompt
    };

    this.https.post(this.OpenAIUrl, payload1)
      .subscribe((response: any) => {
        console.log('API response:', response);
        this.openAIAnswer = response.text.replace(/\n\n/g, '<br>');
        this.isLoadingOpenAI = false;
        this.THOT();
        if(this.enableSearch){
          this.toggleSearch();
        }
      }, error => {
        this.isLoadingOpenAI = false;
      });
  }

  THOT() {
    this.isLoadingTHOT = true;
    const payload2 = {
      temperature: '0',
      model_name: 'gpt4',
      Prompt: this.prompt
    };

    this.https.post(this.THOTUrl, payload2)
      .subscribe((response: any) => {
        console.log('API response:', response);
        let formattedText = response.text
          .replace(/Result:/g, '<br>Result:<br>')
          .replace(/Explanation:/g, '<br>Explanation:<br>')
          .replace(/\n\n/g, '<br>');
       // this.THOTAnswer = formattedText;
       const lines = response?.text?.split('\n');
       const resultLine = lines.find((line: any) => line.startsWith('Result:'));
       const resultExplain = lines.find((line: any) => line.startsWith('Explanation:'));

       let resultValue = '';
       let explanationValue = '';
       if (resultLine) {
        resultValue = resultLine.split('Result:')[1]?.trim(); // Trim leading and trailing whitespace
        const nextNewLineIndex = resultValue.indexOf('\n');
        if (nextNewLineIndex !== -1) {
          resultValue = resultValue.substring(0, nextNewLineIndex);
        }
      }
      
      if (resultExplain) {
        explanationValue = resultExplain.split('Explanation:')[1]?.trim(); // Trim leading and trailing whitespace
        const nextNewLineIndex = explanationValue.indexOf('\n');
        if (nextNewLineIndex !== -1) {
          explanationValue = explanationValue.substring(0, nextNewLineIndex);
        }
      }
       this.THOTAnswer= `${resultValue}<br>${explanationValue}`;
    
        const payload3 = {
          inputPrompt: this.prompt,
          response: this.openAIAnswer
        };
        this.Uncertanity(payload3,"thot");
        this.isLoadingTHOT = false;
      }, error => {
        this.isLoadingTHOT = false;
      });
  }

  Uncertanity(payload:any,thought:any) {
    this.isLoadingUncertainty = true;
    this.https.post(this.UncertaintyUrl, payload)
      .subscribe((response: any) => {
        console.log('Uncertanity response:', response);  
        if(thought == "thot")  {
          this.UncertaintyAIMetric = response;
        }else {
          this.UncertaintyGotMetric = response;
        }
        this.isLoadingUncertainty = false;
        
      //  this.displayMetrics(response);
      }, error => {
        this.isLoadingUncertainty = false;
      });
  }

  displayMetrics(response: any) {
    const metrics = ['uncertainty', 'coherence'];
    let tableHtml = '<table style="border-collapse: collapse; width: 100%;">';
    tableHtml += '<tr><th style="padding: 8px;">Metric</th><th>Score</th><th style="padding: 8px;">Explanation</th><th style="padding: 8px;">Recommendation</th></tr>';

    metrics.forEach(metric => {
      if (response[metric]) {
        tableHtml += `<tr>
          <td style="padding: 8px;">${metric.charAt(0).toUpperCase() + metric.slice(1)}</td>
          <td style="padding: 8px;">${response[metric].score}</td>
          <td style="padding: 8px;">${response[metric].explanation}</td>
          <td style="padding: 8px;">${response[metric].recommendation}</td>
        </tr>`;
      }
    });

    tableHtml += '</table>';
    const metricsTableElement = document.getElementById('metricsTable');
    if (metricsTableElement) {
      metricsTableElement.innerHTML = tableHtml;
    }
  }

  TokenImportance() {
    this.isLoadingTokenImportance = true;
    this.tokenImportanceShowErrorMessage = false;
    const payload5 = {
      inputPrompt: this.prompt,
      modelName: 'GPT',
    };
 
    this.https.post(this.TokenUrl, payload5)
      .subscribe((response: any) => {
        this.tokenImportanceResponse = response;
        this.isLoadingTokenImportance = false;
        this.tokens= this.tokenImportanceResponse?.token_importance_mapping;
        console.log("tokens:",this.tokens)
        this.updatetopTokens();
        this.createTokenBarChart()
        //this.createFrequencyBarChart()        
        this.frequencyDistributionChart();
        this.tokenImportanceShowErrorMessage = false;
      }, error => {
        console.error('API error:', error);
        this.isLoadingTokenImportance = false;
        this.tokenImportanceShowErrorMessage = true;
      });
  }
  sanitizeImage(imageData: string): SafeUrl {
    return this.sanitizer.bypassSecurityTrustUrl('data:image/jpeg;base64,' + imageData);
  }
  GOT() {
    console.log('GOT method called');
    this.isLoadingGOT = true;
    const payload4 = {
      inputPrompt: this.prompt,
      modelName: 'gpt-35-turbo-16k',
    };

    this.https.post(this.GOTUrl, payload4)
      .subscribe((response: any) => {
        this.apiResult = response;
        this.GOTAnswer = response.final_thought.replace(/\n/g, '<br>');
        const payload = {
          inputPrompt: this.prompt,
          response: response.final_thought
        };
      this.Uncertanity(payload,"got");
        this.isLoadingGOT = false;
      }, error => {
        this.isLoadingGOT = false;
      });
  }
  onToggleSearch(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    this.isSerperSelected = inputElement.checked;
    if(this.isSerperSelected){
      this.finalAnswer = this.InternetResponse.internetResponse[0];
    }else {
      this.finalAnswer = this.covFinalAnswer;
    }
  }
  toggleSearch(){
    this.isLoadingSearch= true;
    const payload6 = {
      inputPrompt: this.prompt,
      llm_response: this.openAIAnswer,
    };
    this.https.post(this.InternetUrl, payload6)
    .subscribe((response: any) => {
      this.InternetResponse = response;
      this.InternetSearchMetric = response.metrics[0];
      console.log('API response:', this.InternetSearchMetric);
      this.isLoadingSearch = false;
    }, error => {
      this.isLoadingSearch = false;
    });
  }

  COVRAG() {    
    this.isLoadingCOVRAG = true;
    console.log('COVRAG started, isLoadingCOVRAG:', this.isLoadingCOVRAG);

    const payload7 = {
      complexity: 'simple',
      fileupload: 'true',
      text: this.prompt,
      vectorestoreid: this.ExplanabilityFileId?.id,
    };

    this.https.post(this.COVRAGUrl, payload7)
      .subscribe((response: any) => {
        const covResponse = response.cov_response;      
        this.finalAnswer1 = covResponse.final_answer;      
        let formattedText = covResponse.verification_answers
          .replace(/Question:/g, '<br><br>Question:')
          .replace(/Answer:/g, '<br>Answer:');      
        this.COVRAGResponse = formattedText;      
        console.log('COVRAGResponse response:', this.COVRAGResponse);
        this.isLoadingCOVRAG = false;
        console.log('COVRAG finished, isLoadingCOVRAG:', this.isLoadingCOVRAG);
      }, error => {
        this.isLoadingCOVRAG = false;
        console.log('COVRAG error, isLoadingCOVRAG:', this.isLoadingCOVRAG);
      });
  }
  THOTRAG() {    
    this.isLoadingTHOTRAG = true;
    const payload8 = {
      fileupload: 'true',
      text: this.prompt,
      vectorestoreid: this.ExplanabilityFileId?.id,
    };

    this.https.post(this.THOTRAGUrl, payload8)
      .subscribe((response: any) => {
        this.THOTRAGResponse = response.thot_response;
        this.THOTRAGSource = response['source-name'];
       this.splitFunction();       
        this.isLoadingTHOTRAG = false;
      }, error => {
        this.isLoadingTHOTRAG = false;
      });
  }
  splitFunction(){
    const lines = this.THOTRAGResponse.split('\n');
    let explanationValue = '';
    let isExplanation = false;
    const resultLine = lines.find(line => line.startsWith('Result:'));
    const resultAnswer = lines.find(line => line.startsWith('Answer:'));
    let resultValue;
    if (resultLine) {
       resultValue = resultLine.split('Result:')[1];
    }else if(resultAnswer){
      console.log("resultAnswer::",resultAnswer)
      resultValue = resultAnswer.split('Answer:')[1];
   }
   this.ThotRagResult = resultValue?.replace(/"/g, ''); // Remove the surrounding quotes

    // const resultExplain = lines.find(line => line.includes('Explanation:'));  
    // console.log("resultExplain::",resultExplain) 
    // if (resultExplain) {
    //   let resultValue = resultExplain.split('Explanation:')[1];
    //    resultValue = resultValue?.replace(/"/g, ''); // Remove the surrounding quotes
    //    this.ThotRagExplanation = resultValue?.replace(/\n/g, '<br>');
    // }
    for (const line of lines) {
      if (line.startsWith('Explanation:')) {
        isExplanation = true;
        explanationValue += '<br>' + line.split('Explanation:')[1]?.trim() + '\n';
      } else if (line.startsWith('Source:')) {
        isExplanation = false;
        break;
      } else if (isExplanation) {
        explanationValue += line.trim() + '\n';
      }
    }
    this.ThotRagExplanation = explanationValue.replace(/"/g, '').replace(/\n/g, '<br>');
    console.log('Explanation:', this.ThotRagExplanation);

  }
  updatetopTokens() {
    this.topTokens = this.tokens
      .sort((a: any, b: any) => b.importance_score - a.importance_score);
      this.topTokens = this.topTokens.slice(0, 10);
      (console.log('topTokens:', this.topTokens));
}
createTokenBarChart(): void {
  if (!this.tokens || this.tokens.length === 0) {
      console.log("No tokens available to create the chart.");
      return;
  }
 
  const ctx = document.getElementById('myTokenBarChart') as HTMLCanvasElement;
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
 
  const ctx = document.getElementById('myDistributionBarChart') as HTMLCanvasElement;
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
isEmptyObject(obj: any) {
  if (obj == null || obj == undefined) {
    return true;
  }
  return Object.keys(obj).length === 0;
}
}