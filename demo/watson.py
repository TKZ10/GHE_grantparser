import re
from playwright.sync_api import Playwright, sync_playwright, expect
from urllib.parse import urlparse
import argparse
from pathlib import Path
import csv
import os
from datetime import datetime
import time

def sync_parse(headless_run=True):

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless_run)
    url_link = "https://www.watson.ch/"
    page = browser.new_page()
    page.goto(url_link)
    time.sleep(1)
    o = urlparse(url_link)
    # Accept the cookies
    page.get_by_role("button", name="Akzeptieren").click()

    # Navigate to online safety (or introduce a loop here to go over all sections)
    page.locator('div.watson-navigation').get_by_label("Digital").hover()
    page.get_by_label("Online-Sicherheit").click()
    time.sleep(3)
    # --------------------------------------------------------------------------------------------------------
    watson_clusters = page.locator('div.watson-cluster').filter(has=page.locator('div.watson-card')).all()
    watson_article_links = []
    for watson_cluster in watson_clusters:
        try:
            if not watson_cluster.locator('div.watson-card').count():
                continue
        except:
            continue
        else:
            watson_cards = watson_cluster.locator('div.watson-card').all()
            for watson_card in watson_cards:
                if watson_card.locator('div').nth(0) and watson_card.locator('div').nth(0).get_attribute('data-story-id'):
                    watson_article_links.append(watson_card.locator('div').nth(0).get_by_role('link').get_attribute('href'))
    # limit to the first 10
    watson_article_links = watson_article_links[:10]
    parsed_results = []
    for article_link in watson_article_links:
        try:
            page.goto(article_link, timeout=5_000)
            story_content = page.locator('div.watson-story__content')
            title_lst = story_content.get_by_role('heading').all_text_contents()
            title = " ".join(title_lst).strip()
            tiny_text_lst = story_content.locator('div.watson-snippet__shareBubbles').locator('div.text-xxs').all_text_contents()
            date_published = " ".join(tiny_text_lst).strip()
        except:
            continue
        else:
            # print(f"adding: {(title, date_published, article_link)}")
            parsed_results.append({
                "title":title, 
                "link":article_link,
                "deadline":date_published}
                )   
    
    # print(parsed_results)

    print("DONE")

    browser.close()
    playwright.stop()

    return parsed_results

def save_results_to_csv(output_file_path, results):

    # Generate CSV file name based on current timestamp
    # timestamp="latest"
    csv_file = output_file_path #f"results/parsed_results_{timestamp}.csv"
    
    # Define CSV header based on result structure
    header =  ['title', 'link', 'deadline']

    # Write the results to CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Results saved to {csv_file}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file_name", help=(
        "NAME of the OUTPUT CSV file in the OUTPUT_DIR "
        "directory, by default (almost) same as the script name"
        ) )
    parser.add_argument("--output_dir", help=(
        "OPTIONAL DIRECTORY RELATIVE PATH "
        "by default set to ../results directory"
        ))
    args=parser.parse_args()
    output_dir=args.output_dir
    if output_dir is None:
        output_dir=Path(os.getcwd()).joinpath("results")
    else:
        output_dir=Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file_name=args.output_file_name
    if output_file_name is None:
        output_file_name="Watson" + ".csv"

    output_file_path = output_dir.joinpath(output_file_name)
    parsed_results = sync_parse()
    save_results_to_csv(output_file_path, parsed_results)
    


if __name__=="__main__":
    main()

# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.watson.ch/")
#     page.get_by_role("button", name="Akzeptieren").click()
#     page.get_by_label("Online-Sicherheit").click()
#     page.locator("a").filter(has_text="10Microsoft und US-Justiz:").click()
#     expect(page.get_by_text("20:1204.10.2024, 05:53")).to_be_visible()
#     expect(page.locator("h2").filter(has_text="Microsoft und US-Justiz:")).to_be_visible()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
