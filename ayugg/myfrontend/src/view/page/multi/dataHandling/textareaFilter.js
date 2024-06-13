// input: inputText 전체 output: 필요한부분만 분할하여 nickname을 리스트화
function Filter(text) {
    let textList = [];
    let res = [];
    const regex = /(.+?) #(.+?) \(/;
    
    if (text.trim().length === 0) {
      alert("문자를 입력해주세요.");
    } else {
      if (text.includes("\n")) {
        textList = text.split("\n").filter(Boolean);
        for (let index = 0; index < textList.length; index++) {
          let newData = [];
          if (textList[index].includes("님이 로비에 참가하셨습니다.")) {
            const nameData = textList[index].match(regex);
            if (nameData) {
              newData[0] = nameData[1];
              newData[1] = nameData[2];
              res.push(newData);
            } else {
              console.log("No match found");
            }
          } else {
            newData = textList[index].split("#");
            res.push(newData);
          }
        }
      } else {
        const nameData = text.match(regex);
        let newData = [];
        if (nameData) {
          newData[0] = nameData[1];
          newData[1] = nameData[2];
          res.push(newData);
        } else {
          newData = text.split("#");
          res.push(newData);
        }
      }
    }
    // console.log(res);
    return res;
};

export default Filter;
  