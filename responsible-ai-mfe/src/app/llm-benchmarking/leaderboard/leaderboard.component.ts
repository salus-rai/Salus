/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.css']
})
export class LeaderboardComponent {
  isLoadingTable = true;
  LeaderboardLLMendpoint: any = '';
  constructor(
    public https: HttpClient,
    private _snackBar: MatSnackBar,
    private cdr: ChangeDetectorRef,
    // private logger: NGXLogger
  ) { }
  ngOnInit(): void {
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      if (x != null) {
        this.ip_port = JSON.parse(x)
      }
    }
    this.securityLLM_getLeaderBoard = this.ip_port.result.Security_llm + this.ip_port.result.SecurityLLM_getLeaderboard;
    this.securityLLM_availableDatasets = this.ip_port.result.Security_llm + this.ip_port.result.SecurityLLM_availableDataSets;
    this.securityLLMFairness_leaderboard = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.SecurityLLMF;
    this.externalRobustnessScore = this.ip_port.result.Security_llm + this.ip_port.result.SecurityLLM_ExternalRobustScore;
    this.externalAttackScore = this.ip_port.result.Security_llm + this.ip_port.result.SecurityLLM_ExternalAttackScore;
    this.LLMleaderboardPrivacy = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.SecurityLLMPrivacyLScore;
    this.LLMleaderboardSafety = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.SecurityLLMSafetyLScore;
    this.LLMLeaderboardEthics = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.SecurityLLMEthicsLScore;
    this.LLMLeaderboardTruthfullness = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.SecurityLLMTruthfullnessLScore;
    this.LeaderboardLLMendpoint = this.ip_port.result.SecurityLLMLeaderboard + this.ip_port.result.LeaderboardEndpoint;
    this.getFairnessLeaderboard();
    // this.getExternalRobustnessScore();
    // this.getExternalAttackScore();
    this.getPrivacyScore();
    // this.getSafetyScore();
    this.getEthicsScore();
    this.getTruthfullnessScore();
    this.isLoadingTable = false;
  }

  handleError(error: any) {
    console.log(error)
    console.log(error.status);
    console.log(error.error.detail);
    let message
    if (error.status === 500) {
      message = "Internal Server Error. Please try again later.";
    } else {
      message = error.error.detail || error.error.message || "API has failed";
    }
    const action = 'Close';
    this.openSnackBar(message, action);
  }
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['le-u-bg-black'],
    });
  }

  activeTable = 'Model Fairness'
  options = [
    // { name: 'Model Robustness', value: 'Model Robustness' },
    //{ name: 'Adversarial Robustness', value: 'Adversarial Robustness' },
    { name: 'Model Fairness', value: 'Model-Fairness' },
    { name: 'Model Truthfullness', value: 'Model-Truthfullness' },
    // { name: 'Model Safety', value: 'Model-Safety' },
    { name: 'Model Privacy', value: 'Model-Privacy' },
    { name: 'Model Ethics', value: 'Model-Ethics' },
  ];

  externalRobustnessScore = '';
  externalAttackScore = '';
  LLMleaderboardPrivacy = '';
  LLMleaderboardSafety = '';
  LLMLeaderboardEthics = '';
  LLMLeaderboardTruthfullness = '';
  avaiableDataSetsVariable: any;
  listOfaviablableDataSets: string[] = [];
  columnList: string[] = []
  securityLLM_getLeaderBoard = '';
  securityLLM_availableDatasets = '';
  securityLLMFairness_leaderboard = '';
  leaderboardModelLists: string[] = [];
  leaderBoardData: { [key: string]: { [key: string]: string } } = {};
  leaderboardDataSource: { [key: string]: string }[] = [];
  ip_port: any
  fairness: { [key: string]: { [key: string]: number } }[] = [];
  dataSourceFairness: any[] = [];
  fairnessKeys: string[] = []
  fairnessCol: string[] = [];
  getLeaderboard() {
    this.https.get(this.securityLLM_getLeaderBoard).subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.leaderBoardData = res;
        this.leaderboardModelLists = Object.keys(this.leaderBoardData);
      },
      error => {
        // this.logger.log("Error status",error.status);
        this.handleError(error)
      }
    );
  }
  getAvailableDataSets() {
    this.https.get(this.securityLLM_availableDatasets).subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.avaiableDataSetsVariable = res
        this.getListOfDataSets();
        this.cdr.detectChanges();
      }, error => {
        // this.logger.error("Api call get failed",error);
        this.handleError(error)

      }
    )
  }
  getListOfDataSets() {
    try {
      for (let i = 0; i < this.avaiableDataSetsVariable.length; i++) {
        this.listOfaviablableDataSets.push(this.avaiableDataSetsVariable[i].DatasetName);
      }
      this.leaderboardMethod();
    } catch (error) {
      console.log("method failed",error);
    }
  }
  leaderboardMethod() {
    try {
      if (this.leaderboardModelLists.length != 0) {
        this.columnList = ['Model Name', ...this.listOfaviablableDataSets];
        // this.logger.debug("Leaderboard Column",this.columnList);
        this.leaderboardModelLists.forEach(model => {
          const dict: { [key: string]: string } = {};
          this.columnList.forEach(key => {
            if (key === 'Model Name') {
              dict[key] = model;
            }
            else {
              if (this.leaderBoardData[model][key] !== undefined) {
                dict[key] = this.leaderBoardData[model][key];
              }
              else {
                dict[key] = '--';
              }
            }
          });
          this.leaderboardDataSource.push(dict);
        });
      }
      else {
        this.leaderboardDataSource = [];
      }
    } catch (error) {
      console.log("method failed",error);
    }
  }
  getFairnessLeaderboard() {
    // https://rai-toolkit-dev.az.ad.idemo-ppc.com/api/v1/trustllm/scores/getScores?category=fairness

    this.https.get(this.LeaderboardLLMendpoint + 'scores/getScores?category=fairness').subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.fairness = res;
        console.log("value", this.fairness)
      },
      error => {
        // this.logger.log("Error status",error.status);
        this.handleError(error)
      }
    );
  }
  leaderboardFairnessMethod() {
    try {
      this.fairnessKeys = this.fairness.map((dict) => Object.keys(dict)[0]);
      this.fairnessCol = ['Model_Name', ...Object.keys(this.fairness[0][this.fairnessKeys[0]])];
      for (let i = 0; i < this.fairnessKeys.length; i++) {
        this.dataSourceFairness.push({ ...{ "Model_Name": this.fairnessKeys[i] }, ...this.fairness[i][this.fairnessKeys[i]] })
      }
    } catch (error) {
      console.log("leaderboardFairnessMethod method failed",error);
    }
  }
  dataSourceTruthfullness: any[] = [];
  dataSourceSafety: any[] = [];
  dataSourcePrivacy: any[] = [];
  dataSourceMachineEthics: any[] = [];
  dataSourceRobustness: any[] = []
  dataSourceAttackScore: any[] = [];
  getExternalRobustnessScore() {
    this.https.get(this.externalRobustnessScore).subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourceRobustness = res
        this.cdr.detectChanges();
      }, error => {
        // this.logger.error("Api call get failed for getExternalRobustnessScore method",error);
        this.handleError(error)
      }
    )
  }
  getExternalAttackScore() {
    this.https.get(this.externalAttackScore).subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourceAttackScore = res
        this.cdr.detectChanges();
      }, error => {
        this.handleError(error)
      }
    )
  }
  getPrivacyScore() {
    this.https.get(this.LeaderboardLLMendpoint + 'scores/getScores?category=privacy').subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourcePrivacy = res
        this.cdr.detectChanges();
      }, error => {
        this.handleError(error)
      }
    )
  }
  getSafetyScore() {
    this.https.get(this.LLMleaderboardSafety).subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourceSafety = res
        this.cdr.detectChanges();
      }, error => {
        this.handleError(error)
      }
    )
  }
  getEthicsScore() {
    this.https.get(this.LeaderboardLLMendpoint + 'scores/getScores?category=ethics').subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourceMachineEthics = res
        this.cdr.detectChanges();
      }, error => {
        this.handleError(error)
      }
    )
  }
  getTruthfullnessScore() {
    this.https.get(this.LeaderboardLLMendpoint + 'scores/getScores?category=truthfulness').subscribe(
      (res: any) => {
        // this.logger.info("Api call has been successfull");
        this.dataSourceTruthfullness = res
        this.cdr.detectChanges();
      }, error => {
        this.handleError(error)
      }
    )
  }

  toString(value: any): string {
    return value != null ? String(value) : '';
}
sortColumn: string = '';
currentSortColumn: string = '';
  // sortDirection: boolean = true; // true for ascending, false for descending
  sortDirection: 'asc' | 'desc' = 'asc';
  sortData(column: string): void {
    if (this.currentSortColumn === column) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.currentSortColumn = column;
      this.sortDirection = 'asc';
    }
  
    this.fairness.sort((a, b) => {
      let valueA: any = a[column];
      let valueB: any = b[column];
  
      // Convert to number if the column is 'prefereence_rta'
      if (column === 'prefereence_rta') {
        valueA = parseFloat(valueA.toString()) || 0;
        valueB = parseFloat(valueB.toString()) || 0;
      }
  
      if (valueA < valueB) {
        return this.sortDirection === 'asc' ? -1 : 1;
      } else if (valueA > valueB) {
        return this.sortDirection === 'asc' ? 1 : -1;
      } else {
        return 0;
      }
    });
  }
}
