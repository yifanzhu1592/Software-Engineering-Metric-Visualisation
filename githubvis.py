import pygal
from github import Github
from pprint import pprint

# Get the Github user and their repositories
username = input("Enter a Github Username: ")

try:
    token = input("Enter your personal access token: ")
    git = Github(token)
    user = git.get_user(username)
    print("Valid token. Unlimited access.")
except:
    git = Github()
    user = git.get_user(username)
    print("Invalid token. Limited access.")

repositories = user.get_repos()

# Extract information from the user and their repositories.
languages, months = {}, [0] * 12
months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for repo in repositories:

    language = repo.language
    if language in languages:
        languages[language] = languages[language] + 1
    else:
        languages[language] = 1

    month = int(repo.created_at.strftime("%m"))
    months[month-1] = months[month-1] + 1

# Metric Visualisation.
config = pygal.Config()
config.show_legend = True
config.title_font_size = 50
config.label_font_size = 20
config.show_y_guides = False
config.width = 1350

pie_chart = pygal.Pie(config, inner_radius=.4)
pie_chart.title = f"Most used languages by {user.login}"
for language in languages:
    pie_chart.add(language, languages[language])
pie_chart.render_in_browser()
pie_chart.render_to_file("Most_used_languages.png")

tree_map = pygal.Treemap(config)
tree_map.title = f"{user.login}'s most starred repositories"
for repo in repositories:
    tree_map.add(repo.name, repo.stargazers_count)
tree_map.render
tree_map.render_in_browser()
tree_map.render_to_file("Most_starred_repositories.png")

bar_chart = pygal.Bar(config)
bar_chart.title = f"{user.login}'s repositories created in each month"
bar_chart.x_labels = months_names
bar_chart.add('', months)
bar_chart.render
bar_chart.render_in_browser()
bar_chart.render_to_file("Repositories_created_in_each_month.png")