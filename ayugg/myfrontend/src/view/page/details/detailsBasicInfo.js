import * as styled from "./detailsStyle";

function BasicInfo(props){
  if (!props.data || !props.data.basic || !props.data.champ || !props.data.ranking || !props.data.id) {
    return <div>Loading...</div>;
  }
  const basicRawData = props.data.basic;
  const rankingRawData = props.data.ranking;
  const idData = props.data.id;

  let basicData, rateData;

  let imgUrl;
  let name;
  if (Array.isArray(basicRawData) && basicRawData.length > 0) {
    basicData = basicRawData[0].fields;
    name = basicData.champ_name;
    imgUrl = "https://ddragon.leagueoflegends.com/cdn/" + basicData.champ_version + "/img/champion/" + basicData.champ_img;
  } else {
    console.error("basicRawData is not a valid array or is empty");
    return <div>Error: Invalid data</div>;
  }

  if (Array.isArray(rankingRawData) && rankingRawData.length > 0) {
    for (var i = 0; i < rankingRawData.length; i++){
      var champRankingData = rankingRawData[i].fields;
      var champId = champRankingData.champ_middle_data_img.split('.')[0];

      var winRate = parseFloat(champRankingData.champ_middle_data_win).toFixed(2);
      var pickRate = parseFloat(champRankingData.champ_middle_data_pick).toFixed(2);
      var banRate = parseFloat(champRankingData.champ_middle_data_ban).toFixed(2);

      if(champId == idData){
        rateData = { 'winRate' : winRate, 'pickRate': pickRate, 'banRate': banRate };
        break;
      };
    };
  } else {
    console.error("champRawData is not a valid array or is empty");
    return <div>Error: Invalid champ data</div>;
  }

  return (
    <>
      <styled.BasicInfoStyle>
        <styled.BasicDivStyle $width="100px">
          <styled.BasicImgStyle src={imgUrl} />
        </styled.BasicDivStyle>
        <styled.BasicDivStyle $width="70%" $margin="0 5px 0 5px">
          <styled.BasicDivStyle $width="55%" $display="block">
            <styled.NameSkillStyle>{name}</styled.NameSkillStyle>
            <SkillImg basic={basicData} />
          </styled.BasicDivStyle>
          <styled.BasicDivStyle $width="auto">
            <RateDiv rateData = {rateData} type="winRate"></RateDiv>
            <RateDiv rateData = {rateData} type="pickRate"></RateDiv>
            <RateDiv rateData = {rateData} type="banRate"></RateDiv>
          </styled.BasicDivStyle>
        </styled.BasicDivStyle>
        <styled.BasicDivStyle $width="150px" /> {/* 빈 박스 */}
      </styled.BasicInfoStyle>
    </>
  );
}

function SkillImg(props) {
  let data = props.basic;
  
  function img_src(skill_img){
    return "https://ddragon.leagueoflegends.com/cdn/" + data.champ_version + "/img/spell/" + skill_img;
  }

  function p_img_src(skill_img){
    return "https://ddragon.leagueoflegends.com/cdn/" + data.champ_version + "/img/passive/" + skill_img;
  }

  return (<styled.NameSkillStyle>
    <styled.SkillImgStyle $size="32px" src={p_img_src(data.champion_passive_img)} />
    <styled.SkillImgStyle $size="32px" src={img_src(data.champion_q_img)} />
    <styled.SkillImgStyle $size="32px" src={img_src(data.champion_w_img)} />
    <styled.SkillImgStyle $size="32px" src={img_src(data.champion_e_img)} />
    <styled.SkillImgStyle $size="32px" src={img_src(data.champion_r_img)} />
  </styled.NameSkillStyle>);
}

function RateDiv(props) {
  const rate = props.rateData;
  let type;
  let typeResult;

  switch (props.type){
    case 'winRate' :
      type = "승률";
      typeResult = rate.winRate + "%";
      break;
    case 'pickRate' :
      type = "픽률";
      typeResult = rate.pickRate + "%";
      break;
    case 'banRate' :
      type = "밴률";
      typeResult = rate.banRate + "%";
      break;
    default:
      type = "";
      typeResult = "";
      break;
  }

  return (
    <>
      <styled.RateBoxStyle>
        <styled.RateStyle>{type}</styled.RateStyle>
        <styled.RateStyle $weight="700">{typeResult}</styled.RateStyle>
      </styled.RateBoxStyle>
    </>
  )
}

function NotFoundData() {
  return (
    <styled.NotFoundDivStyle> 수집중 </styled.NotFoundDivStyle>
  )
}

function CounterDiv(props) {
  return (
    <>
      <styled.CounterDivStyle>
        <styled.CounterImgStyle src={props.src}></styled.CounterImgStyle>
        <styled.CounterInfoStyle $margin="5px 0px;"></styled.CounterInfoStyle>
        <styled.CounterInfoStyle $margin="0;">{props.rate}</styled.CounterInfoStyle>
      </styled.CounterDivStyle>
    </>
  );
}

function CounterLiTag(props) {
  if (!props.data || !props.data.basic || !props.data.champ) {
    return <div>Loading...</div>;
  }
  const champRawData = props.data.champ;
  const basicRawData = props.data.basic;

  let basicData, version;

  let imgUrl;
  if (Array.isArray(basicRawData) && basicRawData.length > 0) {
    basicData = basicRawData[0].fields;
    version = basicData.champ_version
    imgUrl = "https://ddragon.leagueoflegends.com/cdn/" + basicData.champ_version + "/img/champion/" + basicData.champ_img;
  } else {
    console.error("basicRawData is not a valid array or is empty");
    return <div>Error: Invalid data</div>;
  }

  let champData, winList, loseList, len;
  if (Array.isArray(champRawData) && champRawData.length > 0) {
    champData = champRawData[0].fields;
    winList = [ champData.detail_win_counter_1, champData.detail_win_counter_2, champData.detail_win_counter_3 ];
    loseList = [ champData.detail_lose_counter_1, champData.detail_lose_counter_2, champData.detail_lose_counter_3 ];
    len = winList.length;
  } else {
    console.error("champRawData is not a valid array or is empty");
    return <div>Error: Invalid champ data</div>;
  }

  let counterList = [];

  function img_src(name){
    var src = "https://ddragon.leagueoflegends.com/cdn/" + version + "/img/champion/" + name + ".png";
    return src
  }

  for(let i = 0; i < len; i++){
    if (props.win === "true") {
      let divBox = winList[i].name !== "imgNull" ? <CounterDiv key={i} src={img_src(winList[i].name)} rate={winList[i].winRate} /> : <NotFoundData />;
      counterList.push(divBox)
    } else {
      let divBox = loseList[i].name !== "imgNull" ? <CounterDiv key={i} src={img_src(loseList[i].name)} rate={loseList[i].winRate} /> : <NotFoundData />;
      counterList.push(divBox)
    }
  }

  return (
    <styled.CounterOlStyle>
      <styled.CounterLiStyle>
        { counterList }
      </styled.CounterLiStyle>
    </styled.CounterOlStyle>
  );
}

export default function FirstArticle(props) {
  return (
    <>
      <styled.OutBoxStyle $height="300px">
        <BasicInfo data={props} />
        <styled.CounterBoxStyle>
          <styled.CounterStyle $back="rgb(49, 49, 79)">
            <div>상대하기 쉬운 챔피언</div>
            <CounterLiTag data={props} win="true"></CounterLiTag>
          </styled.CounterStyle>
          <styled.CounterStyle $back="rgb(108, 65, 65)">
            <div>상대하기 어려운 챔피언</div>
            <CounterLiTag data={props} win="false"></CounterLiTag>
          </styled.CounterStyle>
        </styled.CounterBoxStyle>
      </styled.OutBoxStyle>
    </>
  );
}