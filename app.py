import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title for the Streamlit app
st.title("WhatsApp Chat Analyzer")

# Allow the user to upload a chat file
uploaded_file = st.file_uploader("Choose a WhatsApp chat export file")
if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    # Select a user for analysis
    selected_user = st.selectbox("Show analysis for", user_list)

    if st.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most active days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most active months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

        # Finding the busiest users in the group (Group level)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            top_users, user_stats = helper.most_active_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(top_users.index, top_users.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(user_stats)

        # WordCloud
        st.title("Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        st.image(wc.to_array(), use_container_width=True)

        # Most common words
        most_common_words = helper.most_common_words(selected_user, df)
        st.title('Most Common Words')
        st.bar_chart(most_common_words)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
