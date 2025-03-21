/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
// import { MfeHomeComponent } from './mfe-home/mfe-home.component';
import { Route, RouterModule } from '@angular/router';
import { HomeComponent } from '../home/home.component';
import { UnstructuredTextComponent } from '../unstructured-text/unstructured-text.component';
import { StructuredTextComponent } from '../structured-text/structured-text.component';
import { WorkbenchComponent } from '../workbench/workbench.component';
import { BulkProcessingComponent } from '../bulk-processing/bulk-processing.component';
import { VideoComponent } from '../video/video.component';
import { ImageComponent } from '../image/image.component';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import { ImageParentComponent } from '../image-parent/image-parent.component';
import { ImageDicomComponent } from '../image-dicom/image-dicom.component';
import { SharedModule } from '../shared/shared.module';
import { CodePrivacyComponent } from '../code-privacy/code-privacy.component';
import { DicomViewerModule } from '../dicom-lib/dicom-viewer.module';

import { StructuredTextModalComponent } from '../structured-text-modal/structured-text-modal.component';
import { ImageGenerateComponent } from '../image-generate/image-generate.component';
import { FmModerationComponent } from '../fm-moderation/fm-moderation.component';
import { RequestModerationComponent } from '../fm-moderation/request-moderation/request-moderation.component';
import { ResponseModerationComponent } from '../fm-moderation/response-moderation/response-moderation.component';
import { ResponseComparisonComponent } from '../fm-moderation/response-comparison/response-comparison.component';
import { PrivacyResultComponent } from '../fm-moderation/privacy-result/privacy-result.component';
import { ProfanityResultComponent } from '../fm-moderation/profanity-result/profanity-result.component';
import { ExplainabilityResultComponent } from '../fm-moderation/explainability-result/explainability-result.component';
// import { HomeParentComponent } from '../home-parent/home-parent.component';
import { FairnessResultComponent } from '../fm-moderation/fairness-result/fairness-result.component';

import { HomeParentComponent } from '../home-parent/home-parent.component';
import { AccountMapingComponent } from '../Admin-Configuration/account-maping/account-maping.component';
import { ConfigurationParentComponent } from '../Admin-Configuration/configuration-parent/configuration-parent.component';
import { RecognizersComponent } from '../Admin-Configuration/recognizers/recognizers.component';


import { UseCaseParentComponent } from '../use-case-parent/use-case-parent.component';
import { AiCanvasUsecaseComponent } from '../ai-canvas-usecase/ai-canvas-usecase.component';
// import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RaiCanvasUsecaseComponent } from '../rai-canvas-usecase/rai-canvas-usecase.component';
import { QuestionnaireUsecaseComponent } from '../questionnaire-usecase/questionnaire-usecase.component';
import {MatStepperModule} from '@angular/material/stepper';
import { NewUseCaseComponent } from '../new-use-case/new-use-case.component';
import { UseCaseReportComponent } from '../use-case-report/use-case-report.component';
// import { ImageExplainReportChartComponent } from '../image-explain-report-chart/image-explain-report-chart.component';
// import { ImageReportChartComponent } from '../image-report-chart/image-report-chart.component';

import { RecognizersModalAComponent } from '../Admin-Configuration/recognizers/recognizers-modal-a/recognizers-modal-a.component';
import { AccountsConfigurationComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration.component';
import { ApplicationConfigurationsComponent } from '../Admin-Configuration/application-configurations/application-configurations.component';
import { FMChatConfigurationComponent } from '../Admin-Configuration/fm-chat-configuration/fm-chat-configuration.component';
import { FmParametersComponent } from '../Admin-Configuration/fm-parameters/fm-parameters.component';
import { SafetyParametersComponent } from '../Admin-Configuration/safety-parameters/safety-parameters.component';


import { AiModelsComponent } from '../ai-models/ai-models.component';
import { DataFormComponent } from '../data-form/data-form.component';
import { ModelFormComponent } from '../model-form/model-form.component';
import { ImageReportChartComponent } from '../image-report-chart/image-report-chart.component';
import { AddDataModelComponent } from '../add-data-model/add-data-model.component';
import { AddModelComponent } from '../add-model/add-model.component';
import { VectorFormComponent } from '../vector-form/vector-form.component';
import { AddvectorComponent } from '../addvector/addvector.component';
import { RightSidePopupComponent } from '../fm-moderation/right-side-popup/right-side-popup.component';
import { ResponseModerationHallucinationComponent } from '../fm-moderation/response-moderation-hallucination/response-moderation-hallucination.component';

import { MagnifyImageReportComponent } from '../magnify-image-report/magnify-image-report.component';

import { LlmBenchmarkingComponent } from '../llm-benchmarking/llm-benchmarking.component';
import { ModelValidationComponent } from '../llm-benchmarking/model-validation/model-validation.component';
import { LeaderboardComponent } from '../llm-benchmarking/leaderboard/leaderboard.component';
import { InfosysLeaderboardComponent } from '../llm-benchmarking/infosys-leaderboard/infosys-leaderboard.component';
import { PreviewModalComponent } from '../llm-benchmarking/model-validation/preview-modal/preview-modal.component';


import { AiContentDetectorComponent } from '../ai-content-detector/ai-content-detector.component';

import { UsecaseGuard } from './navigation-guard';
import { StructureTextParentComponent } from '../structure-text-parent/structure-text-parent.component';
import { DifferentialPrivacyComponent } from '../differential-privacy/differential-privacy.component';
// import { HasAnyAuthorityDirective } from './has-any-authority.directive';
import { NgxGraphModule } from '@swimlane/ngx-graph';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { UserManagementComponent } from '../user/user-management/user-management.component';
import { PageRoleAccessComponent } from '../user/user-management/page-role-access/page-role-access.component';
import { CustomTemplateComponent } from '../Admin-Configuration/custom-template/custom-template.component';
import { TemplateDataComponent } from '../Admin-Configuration/template-data/template-data.component';


import { TemplateBasedGuardrailComponent } from '../fm-moderation/request-moderation/template-based-guardrail/template-based-guardrail.component';
import { TemplateBasedGuardrailResponseComponent } from '../fm-moderation/response-moderation/template-based-guardrail-response/template-based-guardrail-response.component';
import { NewUserComponent } from '../new-user/new-user.component';
import { MatDialogModule } from '@angular/material/dialog';
import {MatTreeModule} from '@angular/material/tree';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { AccountsConfigurationModalFmComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration-modal-fm/accounts-configuration-modal-fm.component';
import { AccountsConfigurationModalPrivacyComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration-modal-privacy/accounts-configuration-modal-privacy.component';
import { AccountsConfigurationModalSafetyComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration-modal-safety/accounts-configuration-modal-safety.component';
import { AccountsConfigurationModalCreatePmComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration-modal-create-pm/accounts-configuration-modal-create-pm.component';
import { PrivacyParametersComponent } from '../Admin-Configuration/accounts-configuration/privacy-parameters/privacy-parameters.component';
import { TemplateMappingComponent } from '../Admin-Configuration/template-mapping/template-mapping.component';
import { FormatTemplateNamePipe } from '../pipes/format-template-name.pipe';
import { ImageHashifyRightModalComponent } from '../image/image-hashify-right-modal/image-hashify-right-modal.component';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';
import { AccountsConfigurationModalCreateTemplateUpdateComponent } from '../Admin-Configuration/accounts-configuration/accounts-configuration-modal-create-template-update/accounts-configuration-modal-create-template-update.component';
import { FairnessSideModalComponent } from '../image-generate/fairness-side-modal/fairness-side-modal.component';
import { MultiModalComponent } from '../fm-moderation/request-moderation/multi-modal/multi-modal.component';
import { SemiStructuredTextComponent } from '../semi-structured-text/semi-structured-text.component';
import { LegalAgentComponent } from '../new-use-case/legal-agent/legal-agent.component';

export const remoteRoutes: Route[] = [
  { path: '', component: HomeComponent },
  { path: 'app-use-case-parent', component: UseCaseParentComponent },
  //{ path: 'home', component: HomeComponent },   // Add route
  { path: 'hi', component: ImageParentComponent },   // Add route

];
@NgModule({
  declarations: [
    // MfeHomeComponent,
    HomeComponent,
    UnstructuredTextComponent,
    StructuredTextComponent,
    WorkbenchComponent,
    BulkProcessingComponent,
    VideoComponent,
    ImageComponent,
    ImageParentComponent,
    ImageDicomComponent,
    CodePrivacyComponent,
    StructuredTextModalComponent,
    ImageGenerateComponent,
    FmModerationComponent,
    RequestModerationComponent,
    ResponseModerationComponent,
    ResponseModerationHallucinationComponent,
    ResponseComparisonComponent,
    PrivacyResultComponent,
    ProfanityResultComponent,
    ExplainabilityResultComponent,
    // HomeParentComponent,
    HomeParentComponent,
    ConfigurationParentComponent,
    AccountMapingComponent,
    RecognizersComponent,
    UseCaseParentComponent,
    AiCanvasUsecaseComponent,
    RaiCanvasUsecaseComponent,
    QuestionnaireUsecaseComponent,
    NewUseCaseComponent,
    UseCaseReportComponent,
    RecognizersModalAComponent,
    AccountsConfigurationComponent,
    FMChatConfigurationComponent,
    ApplicationConfigurationsComponent,
    SafetyParametersComponent,
    FmParametersComponent,
    PrivacyParametersComponent,
    TemplateMappingComponent,
    AccountsConfigurationModalPrivacyComponent,
    AccountsConfigurationModalFmComponent,
    AccountsConfigurationModalSafetyComponent,
    AccountsConfigurationModalCreatePmComponent,
    AccountsConfigurationModalCreateTemplateUpdateComponent,
    AiModelsComponent,
    DataFormComponent,
    ModelFormComponent,
    ImageReportChartComponent,
    AddDataModelComponent,
    AddModelComponent,
    VectorFormComponent,
    AddvectorComponent,
    RightSidePopupComponent,
    FairnessResultComponent,
    MagnifyImageReportComponent,
    LlmBenchmarkingComponent,
    ModelValidationComponent,
    LeaderboardComponent,
    InfosysLeaderboardComponent,
    PreviewModalComponent,
    FairnessResultComponent,
    AiContentDetectorComponent,
    StructureTextParentComponent,
    DifferentialPrivacyComponent,
    ChatbotComponent,
    UserManagementComponent,
    PageRoleAccessComponent,
    CustomTemplateComponent,
    TemplateDataComponent,
    TemplateBasedGuardrailComponent,
    TemplateBasedGuardrailResponseComponent,
    NewUserComponent,
    TemplateMappingComponent,
    FormatTemplateNamePipe,
    ImageHashifyRightModalComponent,
    ImageDialogComponent,
    FairnessSideModalComponent,
    MultiModalComponent,
    SemiStructuredTextComponent,
    LegalAgentComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    HttpClientModule,
    DicomViewerModule,
    NgxGraphModule,
    FormsModule,
    ReactiveFormsModule,
    MatStepperModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    NgxSkeletonLoaderModule,
    MatTreeModule,
    MatCheckboxModule,
    RouterModule.forChild(remoteRoutes)    // forChild
  ],
})
export class RemoteMfeModule { }
