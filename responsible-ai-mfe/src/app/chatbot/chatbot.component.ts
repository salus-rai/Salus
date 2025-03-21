/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NonceService } from '../nonce.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit{
  isChatOpen = false;
  prompt = '';
  url :any;
  isLoading: boolean = false;

  sample1='What is privacy in Responsible AI?';
  sample2='What is the Purpose of RAG?';
  sample3='What is FM Moderation in RAI?';

  userMessages: string[] = [];
  botResponses: string[] = [];
  public safeTemplateData!: SafeHtml; 
  constructor(private https: HttpClient,public nonceService:NonceService,private sanitizer: DomSanitizer) {}
  ngOnInit(): void {
  let ip_port: any ;
  if (localStorage.getItem("res") != null) {
    const x = localStorage.getItem("res")
    if (x != null) {
      ip_port = JSON.parse(x)
    }
      // getting list of api from  local storage 
  this.url = ip_port.result.chatBot + ip_port.result.chatBotAnswer;
  }


}
  toggleChat() {
    this.isChatOpen = !this.isChatOpen;
    this.userMessages= [];
    this.botResponses= [];
    this.sample1='What is privacy in Responsible AI?';
    this.sample2='What is the Purpose of RAG?';
    this.sample3='What is FM Moderation in RAI?';
  }

  onBubbleClick(question: string) {
    this.prompt = question;
    this.send();
  }

  send() {
    console.log("url::",this.url)
    const userMessage = this.prompt;
    this.userMessages.push(userMessage);

    const payload = { text: this.prompt };
    this.prompt = '';
    this.isLoading = true;
    this.https.post(this.url, payload).subscribe(response => {
      console.log("chatbotResponse", response);
      const responseArray = response as any[];
      if (responseArray && responseArray.length > 0 && responseArray[0].text) {
        const text = responseArray[0].text;
        const answerMatch = text.match(/Answer:([\s\S]*?)(?=Related questions:|$)/);
        if (answerMatch && answerMatch[1]) {
          const botResponse = answerMatch[1].trim();
          this.botResponses.push(botResponse);
        } else {
          const defaultResponse = "I'm sorry, I cannot answer that as there is no information related";
          this.botResponses.push(defaultResponse);
        }

        const relatedQuestionsMatch = text.match(/Related questions:\n([\s\S]*)/);
        if (relatedQuestionsMatch && relatedQuestionsMatch[1]) {
          const relatedQuestions = relatedQuestionsMatch[1].trim().split('\n').map((q: string) => q.replace(/^\s*\d+\.\s*/, '').trim());
          this.sample1 = relatedQuestions[0];
          this.sample2 = relatedQuestions[1];
          this.sample3 = relatedQuestions[2];
        }
      }
      this.isLoading = false;
    }, error => {
      this.isLoading = false;
    });
  }
  // Function to sanitize the data before it is used
  sanitizeData(data: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(data);
  }
}