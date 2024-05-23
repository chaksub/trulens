/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

/**
 * Specifies additional details on how this span relates to its parent span.
 *
 * Note that this enumeration is experimental and likely to change. See
 * https://github.com/open-telemetry/opentelemetry-specification/pull/226.
 */
export type SpanKind = 0 | 1 | 2 | 3 | 4;
/**
 * Represents the canonical set of status codes of a finished Span.
 */
export type StatusCode = 0 | 1 | 2;

export interface _Master_ {
  Span: Span;
  SpanAgent: SpanAgent;
  SpanEmbedding: SpanEmbedding;
  SpanLLM: SpanLLM;
  SpanMemory: SpanMemory;
  SpanMethodCall: SpanMethodCall;
  SpanOther: SpanOther;
  SpanReranker: SpanReranker;
  SpanRetriever: SpanRetriever;
  SpanRoot: SpanRoot;
  SpanTask: SpanTask;
  SpanTool: SpanTool;
  TransSpanRecordAppCall: TransSpanRecordAppCall;
  SpanUntyped: SpanUntyped;
  TransSpanRecord: TransSpanRecord;
  [k: string]: unknown;
}
/**
 * Base Span type.
 *
 * Smallest unit of recorded activity.
 */
export interface Span {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * An agent invocation.
 */
export interface SpanAgent {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  description: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * An embedding cal.
 */
export interface SpanEmbedding {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  input_text: {
    [k: string]: unknown;
  };
  model_name: {
    [k: string]: unknown;
  };
  embedding: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A generation call to an LLM.
 */
export interface SpanLLM {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  model_name: {
    [k: string]: unknown;
  };
  model_type: {
    [k: string]: unknown;
  };
  temperature: {
    [k: string]: unknown;
  };
  input_messages: {
    [k: string]: unknown;
  };
  input_token_count: {
    [k: string]: unknown;
  };
  output_messages: {
    [k: string]: unknown;
  };
  output_token_count: {
    [k: string]: unknown;
  };
  cost: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A memory call.
 */
export interface SpanMemory {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  memory_type: {
    [k: string]: unknown;
  };
  remembered: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Span which corresponds to a method call.
 *
 * See also temporary development attributes in
 * [TransSpanRecordAppCall][trulens_eval.trace.span.TransSpanRecordCall].
 */
export interface SpanMethodCall {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Other uncategorized spans.
 */
export interface SpanOther {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A reranker call.
 */
export interface SpanReranker {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  query_text: {
    [k: string]: unknown;
  };
  model_name: {
    [k: string]: unknown;
  };
  top_n: {
    [k: string]: unknown;
  };
  input_context_texts: {
    [k: string]: unknown;
  };
  input_context_scores: {
    [k: string]: unknown;
  };
  output_ranks: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A retrieval.
 */
export interface SpanRetriever {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  query_text: {
    [k: string]: unknown;
  };
  query_embedding: {
    [k: string]: unknown;
  };
  distance_type: {
    [k: string]: unknown;
  };
  num_contexts: {
    [k: string]: unknown;
  };
  retrieved_contexts: {
    [k: string]: unknown;
  };
  retrieved_scores: {
    [k: string]: unknown;
  };
  retrieved_embeddings: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A root span encompassing some collection of spans.
 *
 * Does not indicate any particular activity by itself beyond its children.
 */
export interface SpanRoot {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A task invocation.
 */
export interface SpanTask {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A tool invocation.
 */
export interface SpanTool {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  description: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A Span which corresponds to single
 * [RecordAppCall][trulens_eval.schema.record.RecordAppCall].
 *
 * Features references to the call.
 *
 * !!! note
 *     This is a transitional type for the traces work. The non-transitional
 *     fields are being placed in
 *     [SpanMethodCall][trulens_eval.trace.span.SpanMethodCall] instead.
 */
export interface TransSpanRecordAppCall {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  inputs: {
    [k: string]: unknown;
  };
  output: {
    [k: string]: unknown;
  };
  error: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * Generic span type.
 *
 * This represents spans that are being recorded but have not yet been
 * determined to be of a particular type.
 */
export interface SpanUntyped {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
/**
 * A span whose activity was recorded in a record.
 *
 * Features references to the record.
 *
 * !!! note
 *     This is a transitional type for the traces work.
 */
export interface TransSpanRecord {
  /**
   * Name of span.
   */
  name: string;
  /**
   * Kind of span.
   */
  kind?: SpanKind & number;
  /**
   * Status of the span as per OpenTelemetry Span requirements.
   */
  status?: StatusCode & number;
  /**
   * Status description as per OpenTelemetry Span requirements.
   */
  status_description?: string | null;
  /**
   * Timestamp when the span's activity started in nanoseconds since epoch.
   */
  start_timestamp?: number;
  /**
   * Timestamp when the span's activity ended in nanoseconds since epoch.
   *
   * None if not yet ended.
   */
  end_timestamp?: number | null;
  /**
   * Unique immutable identifier for the span.
   */
  context: {
    [k: string]: unknown;
  }[];
  /**
   * Events recorded in the span.
   */
  events?: [unknown, unknown, unknown][];
  /**
   * Attributes of span.
   */
  attributes?: {
    [k: string]: string | boolean | number | string[] | boolean[] | number[];
  };
  /**
   * View into a dict with keys prefixed by some `namespace` string.
   */
  attributes_metadata: {
    [k: string]: unknown;
  };
  tags: {
    [k: string]: unknown;
  };
  span_type: {
    [k: string]: unknown;
  };
  record_id: {
    [k: string]: unknown;
  };
  [k: string]: unknown;
}