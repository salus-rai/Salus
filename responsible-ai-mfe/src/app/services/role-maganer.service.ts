/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { map } from 'rxjs/operators';
import { urlList } from '../urlList';

interface RoleFeatures {
    promptToggle: String;
    selectType: string[];
}

@Injectable({
    providedIn: 'root'
})
export class RoleManagerService {
  //  userRole: any;
    accessiblePages: any;
    authorityAPI = urlList.authorityAPI;
    pages: any;
    constructor(public https: HttpClient) { 
        // for AI PLATFORM
      if(localStorage.getItem("user") != null){
       const userRole = ["ROLE_ADMIN","ROLE_USER"]
       this.getPages(userRole);
       localStorage.setItem("role",JSON.stringify("ROLE_ADMIN"))
       localStorage.setItem("userid",JSON.stringify("admin"))
     } else{
        this.accessiblePages = this.getAccessiblePages();
    }
    }

    getAccessiblePages(): any {
        console.log("PAGESS:::", localStorage.getItem('pages'))
        const pages = localStorage.getItem('pages');
        return pages ? JSON.parse(pages) : [];
    }

    canAccess(page: string): boolean {
        const accessiblePages = this.getAccessiblePages();
        return accessiblePages.includes(page);
    }

    checkPageExists(pageName: string): boolean {
        return this.accessiblePages.hasOwnProperty(pageName);
    }
    checkSubtabExists(parentTabName: string, subtabName: string): boolean {
        if (this.accessiblePages.hasOwnProperty(parentTabName)) {
            return this.accessiblePages[parentTabName].subtabs.hasOwnProperty(subtabName);
        }
        return false;
    }

    checkActiveTabExists(parentTabName: string, subtabName: string, activeTabName: string): boolean {
        if (this.accessiblePages[parentTabName]) {
            if (this.accessiblePages[parentTabName].subtabs && this.accessiblePages[parentTabName].subtabs[subtabName]) {
                return this.accessiblePages[parentTabName].subtabs[subtabName].active.includes(activeTabName);
            } else if (Array.isArray(this.accessiblePages[parentTabName].active)) {
                return this.accessiblePages[parentTabName].active.includes(activeTabName);
            }
        }
        return false;
    }
    
    getSelectedTypeOptions(parentTabName: string, subtabName: string, activeTabName: string) {
        try {
            if (this.accessiblePages[parentTabName] && this.accessiblePages[parentTabName].subtabs[subtabName] && this.accessiblePages[parentTabName].subtabs[subtabName].selectType[activeTabName]) {
                return this.accessiblePages[parentTabName].subtabs[subtabName].selectType[activeTabName];
            }
        } catch (error) {
        }
        return [];
    }

    checkAccessiblePageExists(parentTabName: string, subtabName: string, activeItemName: string): boolean {
        console.log(this.accessiblePages)
        if (this.accessiblePages.hasOwnProperty(parentTabName)) {
            if (this.accessiblePages[parentTabName].hasOwnProperty('subtabs') &&  this.accessiblePages[parentTabName].subtabs.hasOwnProperty(subtabName)) {
                return this.accessiblePages[parentTabName].subtabs[subtabName].includes(activeItemName);
            }else if (this.accessiblePages[parentTabName]) {
                console.log("HEYYYY",this.accessiblePages[parentTabName])
                if (Array.isArray(this.accessiblePages[parentTabName])) {
                    return this.accessiblePages[parentTabName].includes(activeItemName);
                }
            }
        }
        return false;
    }


    getLocalStoreUserRole() {
        let userRole
        if (localStorage.getItem("role") != null) {
            const x = localStorage.getItem("role")
            if (x != null) {
                return userRole = JSON.parse(x)
            }
        }
    }
    getPages(roles: string[]): Promise<string[]> {
        const promises = roles.map(role => {
          return this.https.get<any>(`${this.authorityAPI}?role=${role}`)
            .toPromise()
            .then(response => {
              // Store pages in local storage
              localStorage.setItem('pages', JSON.stringify(response.pages));
              this.accessiblePages = this.getAccessiblePages();
              return Object.keys(response.pages);
            })
            .catch(error => {
              return [];
            });
        });
    
        return Promise.all(promises)
          .then(pagesArray => {
            const combinedPages = pagesArray.reduce((accumulator, pages) => accumulator.concat(this.pages), []);
            return combinedPages;
          })
          .catch(error => {
            return [];
          });
      }
    

}
