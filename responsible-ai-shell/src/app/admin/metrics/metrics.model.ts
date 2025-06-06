/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

export interface Metrics {
  jvm: { [key: string]: JvmMetrics };
  databases: Databases;
  'http.server.requests': HttpServerRequests;
  cache: { [key: string]: CacheMetrics };
  garbageCollector: GarbageCollector;
  services: Services;
  processMetrics: ProcessMetrics;
}

export interface JvmMetrics {
  committed: number;
  max: number;
  used: number;
}

export interface Databases {
  min: Value;
  idle: Value;
  max: Value;
  usage: MetricsWithPercentile;
  pending: Value;
  active: Value;
  acquire: MetricsWithPercentile;
  creation: MetricsWithPercentile;
  connections: Value;
}

export interface Value {
  value: number;
}

export interface MetricsWithPercentile {
  '0.0': number;
  '1.0': number;
  max: number;
  totalTime: number;
  mean: number;
  '0.5': number;
  count: number;
  '0.99': number;
  '0.75': number;
  '0.95': number;
}

export interface HttpServerRequests {
  all: {
    count: number;
  };
  percode: { [key: string]: MaxMeanCount };
}

export interface MaxMeanCount {
  max: number;
  mean: number;
  count: number;
}

export interface CacheMetrics {
  'cache.gets.miss': number;
  'cache.puts': number;
  'cache.gets.hit': number;
  'cache.removals': number;
  'cache.evictions': number;
}

export interface GarbageCollector {
  'jvm.gc.max.data.size': number;
  'jvm.gc.pause': MetricsWithPercentile;
  'jvm.gc.memory.promoted': number;
  'jvm.gc.memory.allocated': number;
  classesLoaded: number;
  'jvm.gc.live.data.size': number;
  classesUnloaded: number;
}

export interface Services {
  [key: string]: {
    [key in HttpMethod]?: MaxMeanCount;
  };
}

export enum HttpMethod {
  Post = 'POST',
  Get = 'GET',
  Put = 'PUT',
  Patch = 'PATCH',
  Delete = 'DELETE',
}

export interface ProcessMetrics {
  'system.cpu.usage': number;
  'system.cpu.count': number;
  'system.load.average.1m'?: number;
  'process.cpu.usage': number;
  'process.files.max'?: number;
  'process.files.open'?: number;
  'process.start.time': number;
  'process.uptime': number;
}

export interface ThreadDump {
  threads: Thread[];
}

export interface Thread {
  threadName: string;
  threadId: number;
  blockedTime: number;
  blockedCount: number;
  waitedTime: number;
  waitedCount: number;
  lockName: string | null;
  lockOwnerId: number;
  lockOwnerName: string | null;
  daemon: boolean;
  inNative: boolean;
  suspended: boolean;
  threadState: ThreadState;
  priority: number;
  stackTrace: StackTrace[];
  lockedMonitors: LockedMonitor[];
  lockedSynchronizers: string[];
  lockInfo: LockInfo | null;
  // custom field for showing-hiding thread dump
  showThreadDump?: boolean;
}

export interface LockInfo {
  className: string;
  identityHashCode: number;
}

export interface LockedMonitor {
  className: string;
  identityHashCode: number;
  lockedStackDepth: number;
  lockedStackFrame: StackTrace;
}

export interface StackTrace {
  classLoaderName: string | null;
  moduleName: string | null;
  moduleVersion: string | null;
  methodName: string;
  fileName: string;
  lineNumber: number;
  className: string;
  nativeMethod: boolean;
}

export enum ThreadState {
  Runnable = 'RUNNABLE',
  TimedWaiting = 'TIMED_WAITING',
  Waiting = 'WAITING',
  Blocked = 'BLOCKED',
  New = 'NEW',
  Terminated = 'TERMINATED',
}