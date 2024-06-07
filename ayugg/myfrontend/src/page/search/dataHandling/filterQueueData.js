

export function FilterQueueData(queueID) {
    // FIND CORRECT QUEUE
    fetch(`http://localhost:8000/search/NekoL`)
    .then(response => response.json())
    .then(data => {
        let newMatches = [];
        let newmatchNum = [];
        for (let i = 0; i < data[0].matches.length; i++) {
            if(data[0].matches[i].info.queueID == queueID){
                newMatches.push(data[0].matches[i]);
                newmatchNum.push(data[0].matchNum[i])
                console.log(newMatches, newmatchNum);
            }
        }

        // console.log(newMatches, newmatchNum);
        let newRes = [newMatches, newmatchNum];
        return newRes;
    })
}