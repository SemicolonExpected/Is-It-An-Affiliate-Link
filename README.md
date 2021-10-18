## getAffiliates.py

run using `getAffiliates.py [listofurls.txt] --ignore [list of ignored domains.txt] --filter`

## getQueryStrings.py

`--filter` filters out google trackers ie gclid, gclsrc by default. You can add or remove filtered out trackers on `line 16`

Takes a textfile of urls and splits them into a dictionary of domains and a list of referer/referral ids pairs associated with the domain

Dictionary format  url => [{rid => referral string}, {rid => referral string}]


## scrapeLinks.py

`scrape({host: [links]})`

I set a timeout of 10 seconds just because with larger datasets it will take forever to run if I dont. There are some sites that take a whole minute to load. Because of this we can't tell what those sites are. 
What I would like is to set up parallel computing over two cores to make this work a lot faster. Splitting it into quarters would actually make this managable. 
<!-- `--filter` filters out facebook and amazon links, we can also define other link patterns to filter out -->

## Pipeline

urls.txt --> getQueryStrings --> check link for affiliate --> scrapeLinks unlabeled links --> check link for affiliates

## Notable Query Parameters in Urls
- `DCLID` is doubleclick
- `h_ad_id` and `gc_id` is [HYROS](https://docs.hyros.com/how-to-connect-your-google-ads-to-hyros/), which tracks ads for conversions gcid specifically is for tracking google ads. Interestingly a lot of the sites that uses the Hyros trackers are webinars or "free book" sites. Interestingly the creator of Hyros is also one of these business "gurus"
- `wickedid` is WickedReports and its users also seem to also be mostly webinars/ free book sites

- [`utm`](https://ga-dev-tools.web.app/ga4/campaign-url-builder/) stuff is adsense campaign related stuff

	- utm_term is paid keywords

- `ref`: if it is on an amazon link surprisingly it is just a regular amazon link. Ref in general (outside of amazon) is most likely an affiliate link
- `aff_c` or `aff_id` is very likely an affiliate link
- `affid` and `afflilate` seem to speak for itself but it could be the companies own affiliate code not a third party's affiliate code
- Sites with `ac` `ai` `cr` `de` `dm` `kw` and `ts` are all use the same site template (loads with 4 rotating semicirlces) `ts:` ytv I believe means tracking source is youtube. These are all not only affiliate marketers, BUT they are Ad Hijackers that masquerade themselves as the company they are advertising for by creating a landing page for the product with a domain that is similar to the product's name
- `contract_id` Sites with this parameter are also ad hijackers but use a different template to the previous group of ad hijackers
- `creativeId` Sites are the affiliates whos sites are dedicated to the topic of the product theyre advertising ie besthealthtips
- `sub4` - `sub8` (sometimes `sub9` and `sub10`) mostly are similar affiliate marketers to `creativeId`. The only exceptions we found was miraclesmanifesterhoodies.com and slotomania
- `subid` looks similar with two exceptions, birchgold and a christian filipino dating site.

- `adp` indicates a group of similar clothing retailers like noracora.com www.hawalili.com justfashionnow.com etc
- `abtf2` sites with this parameter all get content from a site associated with malware in their `loadSuggestions()` function

sites with `search` or `convertri` in their names often were affiliate marketers. The former seems to try to monetize by getting users to click on the advertisement search results that they host. Most of these ad search results are from yahoo. This makes sense because google is known to crack down on advertisement fraud so they could not do this with google ads

Interestingly sites with a `shop` or `store` subdomain did not seem to have many if any affiliates. I believe it is because affiliates like to sell one product, while the shop subdomain implies there is more than one item. `en` and `us` imply multiple sites based on locality/langauge so that is also likely not affiliates. Similarly `investors` as a subdomain hints at the site being a stonk site. `/collections/` usually is a retailer

love-stories-magazine.com is a site that might be an affiliate marketting site for amourfeel.com??

## Notable Outgoing Links
`t.trklv.com` is [Prosper202](https://afflift.com/f/link-directory/prosper202.122/) a free tracker for affiliate marketters - arguably you can use it to track general ad campaigns but it is often used for affiliate marketting. Anysite using those links is an affiliate marketter.

`phr.htrackhq.com` is [TUNE](https://www.tune.com/) (it redirects to phr.hasoffers.com and if you go to just hasoffers.com it redirs to Tune) another affiliate marketing SaaS tool
`scmtrack.com`
`mwchampion.com`
`mwexciting.com`
`clickbank.net` links are definitely affiliate links
`ep20trk.com` apparently potentially malicious content contacts this site
if a link on a page has track in it, I think it is probably it is an affiliate link
`wlg-scrty.com` is a tracking link

One group of affiliates used outgoing links with a `track` subdomain on their domain. When clicked they open the real product's page in a new window.
Another has `offer` as their subdomain. 


<!--- 
A Primer on practices used to do Affiliate Marketting with paid advertisement.

1. Find offer to promote on sites like [OfferVault](offervault.com)
2. Make landing page for that product with affiliate links to or an embeded widget containing the advertised product's content/checkout 
3. Create advertisement on youtube, google, facebook or other advertisin gplatform leading to landing page.
4. ????
5. Profit

The advertiser creates an advertisement that leads to a landing page they created for the product they are advertising to look like they are the legitimate site for the product (merchant site). Depending on the payout model of the offer, a site might do different things.
- In **Pay per Sale** where the advertiser has to make a sale they could create pages with an embedded widgets that links to the merchant site's "add to cart" and "checkout" endpoints. When users try to buy from the advertiser's site they are actually buying the product from the merchant site while still on the fake site the advertiser created. The advertiser makes money because the links to the merchant site contains an affiliate code/tracker and thus the advertiser is credited as having closed the sale. Some 
- In **Pay per Lead** this would be the same except the endpoints would just be for the actions they want users to perform ie sign up for a newsletter/ download something/ watch a video etc
- In **Pay per Click** the advertiser just needs direct affiliate links to the site the merchant wants users to click on. They could also embedd it into their page so it could count as visiting the site when the embedded content loads.


                "feedItemId": "",
                "targetId": "",
                "locInterestMs": "2840",
                "locPhysicalMs": "2840",
                "matchType": "",
                "device": "c",
                "deviceModel": "",
                "deviceType": "desktop",
                "campaignType": "display",

                "pcta": "index-v1b.html",
                "icta": "order-v1.html",
                "iep": "true",
                "loader": "1",
                "fomo": "1",
                "Affid": "3308",
                "s1": "",
                "s2": "",
                "s3": "",
                "s4": "3237",
                "s5": "",
                "domain1": "www.digituplus.com",
                "network_id": "952",
                "DirectLink": "Y",
                "ea": "6C63QHP",
                "eo": "6PJ6MBB",
                "uid": "15307",
                "cc": "3308CC3237"

--->