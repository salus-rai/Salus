/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { SharedModule } from '../../../app/shared/shared.module';
import { MetricsComponent } from './metrics.component';
import { metricsRoute } from './metrics.route';
import { JvmMemoryComponent } from './blocks/jvm-memory/jvm-memory.component';
import { JvmThreadsComponent } from './blocks/jvm-threads/jvm-threads.component';
import { MetricsCacheComponent } from './blocks/metrics-cache/metrics-cache.component';
import { MetricsDatasourceComponent } from './blocks/metrics-datasource/metrics-datasource.component';
import { MetricsEndpointsRequestsComponent } from './blocks/metrics-endpoints-requests/metrics-endpoints-requests.component';
import { MetricsGarbageCollectorComponent } from './blocks/metrics-garbagecollector/metrics-garbagecollector.component';
import { MetricsModalThreadsComponent } from './blocks/metrics-modal-threads/metrics-modal-threads.component';
import { MetricsRequestComponent } from './blocks/metrics-request/metrics-request.component';
import { MetricsSystemComponent } from './blocks/metrics-system/metrics-system.component';

@NgModule({
  imports: [SharedModule, RouterModule.forChild([metricsRoute])],
  declarations: [
    MetricsComponent,
    JvmMemoryComponent,
    JvmThreadsComponent,
    MetricsCacheComponent,
    MetricsDatasourceComponent,
    MetricsEndpointsRequestsComponent,
    MetricsGarbageCollectorComponent,
    MetricsModalThreadsComponent,
    MetricsRequestComponent,
    MetricsSystemComponent,
  ],
})
export class MetricsModule {}
