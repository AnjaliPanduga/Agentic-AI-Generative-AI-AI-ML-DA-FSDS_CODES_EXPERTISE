import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# ---------- Page config ----------
st.set_page_config(page_title="Movie Rating Analysis (Improved UI)", layout="wide")
st.title("🎬 Movie Rating Analysis — Interactive Dashboard")

# ---------- Load dataset ----------
@st.cache_data(show_spinner=True)
def load_data(path):
    df = pd.read_csv(r"C:\Users\pandu\OneDrive\Documents\Desktop\NIT\datasets\Movie-Rating.csv")
    # normalize column names that your notebook expects
    rename_map = {
        'Budget (million $)': 'BudgetMillions',
        'Rotten Tomatoes Ratings %': 'CriticRating',
        'Audience Ratings %': 'AudienceRating',
        'Year of release': 'Year'
    }
    # only rename keys that exist
    existing_rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
    if existing_rename_map:
        df = df.rename(columns=existing_rename_map)
    # if other variations exist, try some fuzzy alternatives
    if 'BudgetMillion' in df.columns and 'BudgetMillions' not in df.columns:
        df = df.rename(columns={'BudgetMillion': 'BudgetMillions'})
    # convert year to int if possible
    if 'Year' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    return df

DATA_PATH = "/mnt/data/Movie-Rating.csv"  # your uploaded CSV path
movies = load_data(DATA_PATH)

# Check required columns and show helpful message if missing
required_cols = ['BudgetMillions', 'CriticRating', 'AudienceRating', 'Year', 'Genre', 'Film']
missing = [c for c in required_cols if c not in movies.columns]

if missing:
    st.warning(
        f"The dataset is missing expected columns: {missing}. "
        "I will attempt to proceed using available columns. "
        "If visuals look wrong, ensure the CSV contains the columns from your notebook."
    )

# ---------- Sidebar controls ----------
st.sidebar.header("Controls & Filters")

# Genre filter (if exists)
if 'Genre' in movies.columns:
    genre_list = np.append(['All'], np.sort(movies['Genre'].dropna().unique()))
    selected_genre = st.sidebar.selectbox("Genre", genre_list, index=0)
else:
    selected_genre = 'All'

# Year filter
if 'Year' in movies.columns:
    min_year = int(movies['Year'].min()) if movies['Year'].notna().any() else 2000
    max_year = int(movies['Year'].max()) if movies['Year'].notna().any() else 2020
    selected_years = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year))
else:
    selected_years = None

# Budget range filter
if 'BudgetMillions' in movies.columns:
    min_b = float(np.nanmin(movies['BudgetMillions']))
    max_b = float(np.nanmax(movies['BudgetMillions']))
    selected_budget = st.sidebar.slider("Budget (millions)", min_b, max_b, (min_b, max_b))
else:
    selected_budget = None

# Apply filters to df used for plots
df = movies.copy()
if selected_genre != 'All' and 'Genre' in df.columns:
    df = df[df['Genre'] == selected_genre]
if selected_years and 'Year' in df.columns:
    df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
if selected_budget and 'BudgetMillions' in df.columns:
    df = df[(df['BudgetMillions'] >= selected_budget[0]) & (df['BudgetMillions'] <= selected_budget[1])]

# ---------- Tabs on top (grid layout inside each tab) ----------
tabs = st.tabs([
    "Dataset",
    "KDE Plots",
    "Violin Plots",
    "Box & Swarm",
    "Scatter & Regression",
    "Count & Bar",
    "FacetGrid / Genre-wise",
    "Jointplots & Pairplot",
    "Heatmap & Correlations",
    "Summary & Insights"
])

# ---------- Tab 1: Dataset ----------
with tabs[0]:
    st.subheader("Dataset Preview")
    st.dataframe(movies.head(100))
    st.markdown(f"**Rows:** {movies.shape[0]}  —  **Columns:** {movies.shape[1]}")
    st.download_button("Download filtered data (CSV)", df.to_csv(index=False), file_name="filtered_movies.csv")

# ---------- Helper function to render a figure in a 2x2 grid using st.columns ----------
def render_grid(plots_funcs):
    """
    plots_funcs: list of plotting functions that accept an Axes or return a Matplotlib Figure.
    We show them in a 2x2 grid per page (per call).
    """
    n = len(plots_funcs)
    i = 0
    while i < n:
        # create a row with two columns (each will contain two plots vertically)
        col1, col2 = st.columns(2, gap="large")
        for col in (col1, col2):
            if i >= n:
                break
            # inside each column place a small 2-row grid (so final looks like 2x2 overall)
            with col:
                fig = plots_funcs[i]()  # each func returns a Matplotlib Figure
                st.pyplot(fig, clear_figure=True)
                i += 1

# ---------- Utility small fig wrapper to standardize size ----------
def fig_wrapper(plot_fn, figsize=(6,4)):
    fig, ax = plt.subplots(figsize=figsize)
    plot_fn(ax)
    fig.tight_layout()
    return fig

# ---------- Tab 2: KDE Plots ----------
with tabs[1]:
    st.subheader("KDE Plots (Grid)")
    plots = []

    # KDE 1: Budget vs Audience
    if 'BudgetMillions' in df.columns and 'AudienceRating' in df.columns:
        def p1(ax):
            sns.kdeplot(x=df['BudgetMillions'], y=df['AudienceRating'], fill=True, cmap='inferno', ax=ax)
            ax.set_xlim(-20, 160)
            ax.set_title("Budget vs Audience Rating KDE")
        plots.append(lambda p=p1: fig_wrapper(p, figsize=(7,5)))

    # KDE 2: Budget vs Critic
    if 'BudgetMillions' in df.columns and 'CriticRating' in df.columns:
        def p2(ax):
            sns.kdeplot(x=df['BudgetMillions'], y=df['CriticRating'], fill=True, cmap='inferno', ax=ax)
            ax.set_xlim(-20, 160)
            ax.set_title("Budget vs Critic Rating KDE")
        plots.append(lambda p=p2: fig_wrapper(p, figsize=(7,5)))

    # KDE 3: Critic vs Audience (density)
    if 'CriticRating' in df.columns and 'AudienceRating' in df.columns:
        def p3(ax):
            sns.kdeplot(x=df['CriticRating'], y=df['AudienceRating'], fill=True, cmap='Blues_r', ax=ax)
            ax.set_title("Critic vs Audience Rating KDE")
        plots.append(lambda p=p3: fig_wrapper(p, figsize=(7,5)))

    # KDE 4: Budget distribution by Genre (overlay)
    if 'BudgetMillions' in df.columns and 'Genre' in df.columns:
        def p4(ax):
            # plot KDE per genre (limit to top 4 genres for clarity)
            top_genres = df['Genre'].value_counts().nlargest(4).index
            for g in top_genres:
                subset = df[df['Genre'] == g]
                if subset['BudgetMillions'].dropna().shape[0] > 1:
                    sns.kdeplot(subset['BudgetMillions'], label=g, ax=ax)
            ax.legend()
            ax.set_title("Budget distribution — top genres")
        plots.append(lambda p=p4: fig_wrapper(p, figsize=(7,5)))

    if plots:
        render_grid(plots)
    else:
        st.info("Required columns for KDE plots are not available in the filtered data.")

# ---------- Tab 3: Violin Plots ----------
with tabs[2]:
    st.subheader("Violin Plots (Grid)")
    plots = []

    # Violin 1: CriticRating by Year (for selected genre)
    if 'CriticRating' in df.columns and 'Year' in df.columns:
        def p1(ax):
            sns.violinplot(data=df, x='Year', y='CriticRating', inner='quartile', cut=0, ax=ax)
            ax.set_title("Critic Rating by Year")
            for label in ax.get_xticklabels():
                label.set_rotation(45)
        plots.append(lambda p=p1: fig_wrapper(p, (10,4)))

    # Violin 2: AudienceRating by Genre (top genres)
    if 'AudienceRating' in df.columns and 'Genre' in df.columns:
        def p2(ax):
            top = df['Genre'].value_counts().nlargest(6).index
            sns.violinplot(data=df[df['Genre'].isin(top)], x='Genre', y='AudienceRating', inner='quartile', ax=ax)
            ax.set_title("Audience Rating by Genre (top 6)")
            for label in ax.get_xticklabels():
                label.set_rotation(45)
        plots.append(lambda p=p2: fig_wrapper(p, (10,4)))

    # Violin 3: Budget by Genre (if present)
    if 'BudgetMillions' in df.columns and 'Genre' in df.columns:
        def p3(ax):
            top = df['Genre'].value_counts().nlargest(6).index
            sns.violinplot(data=df[df['Genre'].isin(top)], x='Genre', y='BudgetMillions', ax=ax)
            ax.set_title("Budget by Genre (top 6)")
            for label in ax.get_xticklabels():
                label.set_rotation(45)
        plots.append(lambda p=p3: fig_wrapper(p, (10,4)))

    if plots:
        render_grid(plots)
    else:
        st.info("Required columns for Violin plots are missing.")

# ---------- Tab 4: Box & Swarm ----------
with tabs[3]:
    st.subheader("Boxplots & Swarmplots (Grid)")
    plots = []

    # Boxplot: Critic by Genre
    if 'CriticRating' in df.columns and 'Genre' in df.columns:
        def p1(ax):
            sns.boxplot(data=df, x='Genre', y='CriticRating', ax=ax)
            ax.set_title("Critic Rating by Genre (boxplot)")
            for t in ax.get_xticklabels():
                t.set_rotation(45)
        plots.append(lambda p=p1: fig_wrapper(p, (10,4)))

    # Swarmplot: Audience by Genre (top 6)
    if 'AudienceRating' in df.columns and 'Genre' in df.columns:
        def p2(ax):
            top = df['Genre'].value_counts().nlargest(6).index
            sns.swarmplot(data=df[df['Genre'].isin(top)], x='Genre', y='AudienceRating', ax=ax, size=3)
            ax.set_title("Audience Rating by Genre (swarm)")
            for t in ax.get_xticklabels():
                t.set_rotation(45)
        plots.append(lambda p=p2: fig_wrapper(p, (10,4)))

    # Boxplot: Budget by Year (if Budget present)
    if 'BudgetMillions' in df.columns and 'Year' in df.columns:
        def p3(ax):
            sns.boxplot(data=df, x='Year', y='BudgetMillions', ax=ax)
            ax.set_title("Budget by Year (boxplot)")
            for t in ax.get_xticklabels():
                t.set_rotation(45)
        plots.append(lambda p=p3: fig_wrapper(p, (10,4)))

    if plots:
        render_grid(plots)
    else:
        st.info("Required columns for box/swarm plots are missing.")

# ---------- Tab 5: Scatter & Regression ----------
with tabs[4]:
    st.subheader("Scatter & Regression (Grid)")
    plots = []

    # Scatter: Budget vs Audience
    if 'BudgetMillions' in df.columns and 'AudienceRating' in df.columns:
        def p1(ax):
            sns.scatterplot(data=df, x='BudgetMillions', y='AudienceRating', hue='Genre' if 'Genre' in df.columns else None, ax=ax)
            sns.regplot(data=df, x='BudgetMillions', y='AudienceRating', scatter=False, ax=ax, truncate=True)
            ax.set_xlim(-20, 160)
            ax.set_title("Budget vs Audience (scatter + regression)")
        plots.append(lambda p=p1: fig_wrapper(p, (7,5)))

    # Scatter: Budget vs Critic
    if 'BudgetMillions' in df.columns and 'CriticRating' in df.columns:
        def p2(ax):
            sns.scatterplot(data=df, x='BudgetMillions', y='CriticRating', hue='Genre' if 'Genre' in df.columns else None, ax=ax)
            sns.regplot(data=df, x='BudgetMillions', y='CriticRating', scatter=False, ax=ax, truncate=True)
            ax.set_xlim(-20, 160)
            ax.set_title("Budget vs Critic (scatter + regression)")
        plots.append(lambda p=p2: fig_wrapper(p, (7,5)))

    # Scatter: Critic vs Audience with marker size by Budget
    if 'CriticRating' in df.columns and 'AudienceRating' in df.columns and 'BudgetMillions' in df.columns:
        def p3(ax):
            size = (df['BudgetMillions'].fillna(df['BudgetMillions'].median()) - df['BudgetMillions'].min()) + 1
            sns.scatterplot(data=df, x='CriticRating', y='AudienceRating', size=size, legend=False, ax=ax)
            ax.set_title("Critic vs Audience (marker size ~ Budget)")
        plots.append(lambda p=p3: fig_wrapper(p, (7,5)))

    if plots:
        render_grid(plots)
    else:
        st.info("Not enough columns for scatter/regression plots.")

# ---------- Tab 6: Count & Bar Plots ----------
with tabs[5]:
    st.subheader("Countplots & Bar Charts (Grid)")
    plots = []

    # Countplot: Genre counts
    if 'Genre' in df.columns:
        def p1(ax):
            order = df['Genre'].value_counts().index
            sns.countplot(y='Genre', data=df, order=order, ax=ax)
            ax.set_title("Movie counts by Genre")
        plots.append(lambda p=p1: fig_wrapper(p, (7,5)))

    # Barplot: Average AudienceRating by Genre (top 8)
    if 'AudienceRating' in df.columns and 'Genre' in df.columns:
        def p2(ax):
            top = df.groupby('Genre')['AudienceRating'].mean().sort_values(ascending=False).head(8)
            sns.barplot(x=top.values, y=top.index, ax=ax)
            ax.set_title("Avg Audience Rating by Genre (top 8)")
        plots.append(lambda p=p2: fig_wrapper(p, (7,5)))

    # Barplot: Average CriticRating by Year
    if 'CriticRating' in df.columns and 'Year' in df.columns:
        def p3(ax):
            avg_year = df.groupby('Year')['CriticRating'].mean().dropna()
            sns.barplot(x=avg_year.index.astype(str), y=avg_year.values, ax=ax)
            ax.set_title("Avg Critic Rating by Year")
            for t in ax.get_xticklabels():
                t.set_rotation(45)
        plots.append(lambda p=p3: fig_wrapper(p, (10,4)))

    if plots:
        render_grid(plots)
    else:
        st.info("No categorical columns found for count/bar plots.")

# ---------- Tab 7: FacetGrid / Genre-wise ----------
with tabs[6]:
    st.subheader("FacetGrid & Genre-wise Visuals")
    plots = []

    # FacetGrid example: AudienceRating over Year for genres (sample top 4)
    if 'AudienceRating' in df.columns and 'Genre' in df.columns and 'Year' in df.columns:
        def p1():
            top = df['Genre'].value_counts().nlargest(4).index
            g = sns.FacetGrid(df[df['Genre'].isin(top)], col="Genre", col_wrap=2, height=3.5, sharey=True)
            g.map(sns.lineplot, "Year", "AudienceRating")
            g.set_titles("{col_name}")
            fig = g.fig
            fig.tight_layout()
            return fig
        plots.append(p1)

    # FacetGrid scatter: Critic vs Audience by Genre
    if 'CriticRating' in df.columns and 'AudienceRating' in df.columns and 'Genre' in df.columns:
        def p2():
            top = df['Genre'].value_counts().nlargest(6).index
            g = sns.FacetGrid(df[df['Genre'].isin(top)], col="Genre", col_wrap=3, height=3.5)
            g.map_dataframe(sns.scatterplot, "CriticRating", "AudienceRating")
            g.set_axis_labels("Critic", "Audience")
            fig = g.fig
            fig.tight_layout()
            return fig
        plots.append(p2)

    # Render facet plots (each returns a Matplotlib Figure)
    if plots:
        i = 0
        for f in plots:
            fig = f()
            st.pyplot(fig, clear_figure=True)
    else:
        st.info("No data to create FacetGrid visuals.")

# ---------- Tab 8: Jointplots & Pairplot ----------
with tabs[7]:
    st.subheader("Jointplots & Pairplot")
    # We'll show multiple jointplots; each created with seaborn and returned as Figure
    jp_plots = []

    if 'BudgetMillions' in df.columns and 'AudienceRating' in df.columns:
        def j1():
            g = sns.jointplot(x='BudgetMillions', y='AudienceRating', data=df, kind='hex', height=6, marginal_kws=dict(bins=25))
            g.fig.suptitle("Jointplot: Budget vs Audience (hex)")
            g.fig.tight_layout()
            return g.fig
        jp_plots.append(j1)

    if 'CriticRating' in df.columns and 'AudienceRating' in df.columns:
        def j2():
            g = sns.jointplot(x='CriticRating', y='AudienceRating', data=df, kind='kde', height=6, fill=True)
            g.fig.suptitle("Jointplot: Critic vs Audience (kde)")
            g.fig.tight_layout()
            return g.fig
        jp_plots.append(j2)

    if len(df.select_dtypes(include=[np.number]).columns) >= 3:
        def pairp():
            cols = df.select_dtypes(include=[np.number]).columns[:5]  # limit size for performance
            g = sns.pairplot(df[cols].dropna().sample(min(300, len(df))), diag_kind='hist', corner=True)
            g.fig.suptitle("Pairplot (sampled numeric cols)")
            g.fig.tight_layout()
            return g.fig
        jp_plots.append(pairp)

    if jp_plots:
        for fn in jp_plots:
            fig = fn()
            st.pyplot(fig, clear_figure=True)
    else:
        st.info("Not enough numeric columns for jointplots/pairplot.")

# ---------- Tab 9: Heatmap & Correlations ----------
with tabs[8]:
    st.subheader("Correlation Heatmap & Summary Stats")
    if df.select_dtypes(include=[np.number]).shape[1] >= 2:
        corr = df.select_dtypes(include=[np.number]).corr()
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", ax=ax)
        ax.set_title("Correlation heatmap (numeric features)")
        st.pyplot(fig, clear_figure=True)

        # summary stats
        st.markdown("**Summary statistics for numeric columns**")
        stats = df.select_dtypes(include=[np.number]).describe().T
        st.dataframe(stats)
    else:
        st.info("Not enough numeric columns to compute correlations.")

# ---------- Tab 10: Summary & Insights ----------
with tabs[9]:
    st.subheader("Automated Insights & Summary")
    st.markdown("**Top-level KPIs**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total movies", movies.shape[0])
    if 'Genre' in movies.columns:
        c2.metric("Unique genres", movies['Genre'].nunique())
    else:
        c2.metric("Unique genres", "N/A")
    if 'BudgetMillions' in movies.columns:
        c3.metric("Avg Budget (M)", f"{movies['BudgetMillions'].mean():.2f}")
    else:
        c3.metric("Avg Budget (M)", "N/A")
    if 'AudienceRating' in movies.columns:
        c4.metric("Avg Audience Rating", f"{movies['AudienceRating'].mean():.2f}")
    else:
        c4.metric("Avg Audience Rating", "N/A")

    st.markdown("**Top insights (automatically generated)**")
    # simple automated insights:
    insights = []
    if 'Genre' in movies.columns:
        top_genre = movies['Genre'].value_counts().idxmax()
        insights.append(f"- Most common genre: **{top_genre}**")
    if 'AudienceRating' in movies.columns:
        top_aud = movies.loc[movies['AudienceRating'].idxmax()] if movies['AudienceRating'].notna().any() else None
        if top_aud is not None and 'Title' in movies.columns:
            insights.append(f"- Highest audience-rated movie: **{top_aud['Title']}** ({top_aud['AudienceRating']})")
    if 'CriticRating' in movies.columns:
        top_cr = movies.loc[movies['CriticRating'].idxmax()] if movies['CriticRating'].notna().any() else None
        if top_cr is not None and 'Title' in movies.columns:
            insights.append(f"- Highest critic-rated movie: **{top_cr['Title']}** ({top_cr['CriticRating']})")
    # show some
    if insights:
        for it in insights:
            st.markdown(it)
    else:
        st.info("Not enough data to generate automated insights.")

    st.markdown("---")
    st.info("This dashboard reproduces and improves the visualizations from your notebook in a tabbed, grid layout. "
            "If you want any specific plot tweaked (colors, labels, sizes) or want a dedicated tab for a single plot, tell me which one and I'll change it.")

# ---------- End ----------
st.markdown("Made with ❤️  — Streamlit + Seaborn + Matplotlib")