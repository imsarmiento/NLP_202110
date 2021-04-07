const apiKey = "7a7886097a3c49fbb2921ac66c16c3de"
const NewsAPI = require('newsapi');
const newsapi = new NewsAPI(apiKey);
const fs = require('fs')

const query = "Pandemic";
const fromDates = [];
const toDates = [];

for(let m = 3; m <= 4; m++){
    for(let i = 1; i <= 31; i++){
        if(m===3 && i < 6) continue;
        if(m===4 && i > 6) break;
        fromDates.unshift(`2021-0${m}-${i}`);
        toDates.unshift(`2021-0${m}-${i}`)
    }
}
fromDates.shift();
toDates.pop();


console.log(fromDates.length, toDates.length)

const newsReader = async () => {

    for(let i = fromDates.length-1; i >= 0; i-- ){
        fromDate = fromDates[i];
        toDate = toDates[i];
        try{
        res = await newsapi.v2.everything({
            q: query,
            from: fromDate,
            to: toDate
        })
        const articles = res.articles;
        const jsonifyArticles = JSON.stringify(articles);
        fs.writeFileSync(`./NewsApi/${query}-${fromDate}-${toDate}.json`, jsonifyArticles);
        } catch(e){
            console.error(e);
        }
    }
}

// newsReader();
