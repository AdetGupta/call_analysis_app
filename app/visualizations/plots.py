import plotly.express as px
import plotly.graph_objects as go

def plot_overtalk(merged):
   fig = px.bar(
        merged,
        x="call_id",
        y=["Agent_overtalk", "Customer_overtalk"],
        title="Overtalk(%)",
        barmode="stack"
    )
   fig.update_layout(
       xaxis=dict(title="Calls", showticklabels=False)  # hide tick labels, keep title
   )
   return fig

def plot_silence(merged):
    fig = px.bar(
        merged,
        x="call_id",
        y=["Agent_silence", "Customer_silence"],
        title="Silence(%)",
        barmode="stack"
    )
    fig.update_layout(
        xaxis=dict(title="Calls", showticklabels=False)  # hide tick labels, keep title
    )
    return fig


def plot_duration_distribution(merged):
    fig =  px.histogram(
        merged, x="total_duration", nbins=20, title="Distribution of Call Durations"
    )
    fig.update_layout(
        xaxis_title="Call Duration (seconds)",
        yaxis_title="Number of Calls"
    )
    return fig

def plot_overtalk_silence_box(merged):
    return px.box(
        merged, y=["Overall_overtalk", "Overall_silence"], title="Overtalk vs Silence Spread"
    )


def plot_profanity_pie(merged):
    num_profane = merged["is_profane"].sum()
    total_calls = len(merged)
    values = [num_profane, total_calls - num_profane]
    fig = go.Figure(data=[go.Pie(
        labels=["Profane Calls", "Clean Calls"],
        values=values,
        hole=0.4
    )])
    fig.update_traces(marker=dict(colors=["#ef476f", "#06d6a0"]))
    fig.update_layout(title="Profanity Presence")
    return fig


def plot_privacy_pie(merged):
    num_privacy = merged["privacy_violation"].sum()
    total_calls = len(merged)
    values = [num_privacy, total_calls - num_privacy]
    fig = go.Figure(data=[go.Pie(
        labels=["Privacy Violations", "Compliant Calls"],
        values=values,
        hole=0.4
    )])
    fig.update_traces(marker=dict(colors=["#ffd166", "#118ab2"]))
    fig.update_layout(title="Privacy Violations Overview")
    return fig


def plot_duration_vs_overtalk(merged):
    return px.scatter(
        merged,
        x="total_duration",
        y="Overall_overtalk",
        color="Overall_silence",
        hover_data=["call_id"],
        title="Call Duration vs Overtalk (%)"
    )


def plot_correlation_heatmap(merged):
    numeric_df = merged.select_dtypes(include=["number"])
    if numeric_df.empty:
        return None
    return px.imshow(numeric_df.corr(), text_auto=True, title="Feature Correlation Heatmap")