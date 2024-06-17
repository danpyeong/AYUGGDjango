import * as styled from "./champsStyle";
import { getChampionRanking } from "../../../model/api/champions";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { changeLine, changeTier, changeVersion } from "../../../redux/store";


function OptionTierButton() {
  const tier = useSelector((state)=>{ return state.rankingTier })
  const [tierList, setTierList] = useState();
  const [props, setProps] = useState("close");
  let dispatch = useDispatch();

  useEffect(()=>{
    setTierList(OptionList(props))
  },[props])

  const openOption = () => {
    props === "open" ? setProps("close") : setProps("open");
    setTierList(OptionList(props))
  };

  function OptionList(props) {
    const tierList = ["Challenger", "Grandmaster", "Master", "DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"];      
    
    let list = tierList.map((key, index) => {
      const src = "/assets/images/tier/" + key.toLowerCase() + ".png"

      return (
        <styled.OptionButtonStyle key={index} onClick={() => dispatch(changeTier(key))}>
          <styled.TierImgBox>
            <styled.OptionListTierImg src={src} $sizes="24px"/>
          </styled.TierImgBox>
          {key}
        </styled.OptionButtonStyle>
      )
    })
  
    return (
      <styled.OptionListBox $state={props}>
        {list}
      </styled.OptionListBox>
    )
  }

  return <>
    <styled.SelectButtonStyle onClick={openOption}>
      {tier}
      <styled.ArrowDown></styled.ArrowDown>
      {tierList}
    </styled.SelectButtonStyle>
  </>;
}

function OptionVersionButton() {
  const ver = useSelector((state)=>{ return state.rankingVersion })
  const [verList, setVerList] = useState();
  const [props, setProps] = useState("close");
  let dispatch = useDispatch();

  useEffect(()=>{
    setVerList(OptionList(props))
  },[props])

  const openOption = () => {
    props === "open" ? setProps("close") : setProps("open");
    setVerList(OptionList(props))
  };

  function OptionList(props) {
    const verList = ["14.11.1", "14.10.1"];      
    
    let list = verList.map((key, index) => <styled.OptionButtonStyle key={index} onClick={() => dispatch(changeVersion(key))}> {key} </styled.OptionButtonStyle>)
  
    return (
      <styled.OptionListBox $state={props}>
        {list}
      </styled.OptionListBox>
    )
  }

  return <>
    <styled.SelectButtonStyle onClick={openOption}>
      {ver}
      <styled.ArrowDown></styled.ArrowDown>
    </styled.SelectButtonStyle>
  </>;
}

function LineButton() {
  const line = useSelector((state)=>{ return state.rankingLine })
  let dispatch = useDispatch();
  const lineList = [{ "name" : "탑", "line" : "TOP" },
  { "name" : "정글", "line" : "JUNGLE" },
  { "name" : "미드", "line" : "MIDDLE" },
  { "name" : "바텀", "line" : "BOTTOM" },
  { "name" : "서폿", "line" : "UTILITY" }];

  let list = lineList.map((data, index) => <styled.LineButtonStyle key={index} $line={data.line} $path={line} onClick={() => dispatch(changeLine(data.line))}>{data.name}</styled.LineButtonStyle>)

  return (
  <styled.LineButtonBox>
    {list}
  </styled.LineButtonBox>)
}

function NavTitle() {
  return (
    <>
      <styled.RankingTitleBox>
        <styled.RankingTitle $seq="start" $width="10%">
          순위
        </styled.RankingTitle>
        <styled.RankingTitle $width="30%">
          챔피언
        </styled.RankingTitle>
        <styled.RankingTitle $width="10%">
          티어
        </styled.RankingTitle>
        <styled.RankingTitle $width="10%">
          승률
        </styled.RankingTitle>
        <styled.RankingTitle $width="10%">
          픽률
        </styled.RankingTitle>
        <styled.RankingTitle $width="10%">
          밴율
        </styled.RankingTitle>
        <styled.RankingTitle $seq="end" $width="20%">
          카운터
        </styled.RankingTitle>
      </styled.RankingTitleBox>
    </>
  )
}

export function Ranking() {
  const [rank, setRank] = useState([]);

  let line = useSelector((state)=>{ return state.rankingLine })
  let tier = useSelector((state)=>{ return state.rankingTier })
  let ver = useSelector((state)=>{ return state.rankingVersion })
  
  useEffect(()=>{
      getChampionRanking(tier, line, ver)
      .then((data)=>{
        setRank(JSON.parse(data));
      })
  },[tier, line, ver]);

  let win_calc_list = [];
  let pick_calc_list = [];
  let ban_calc_list = [];

  function push_rate_list(){ rank.map((rawdata, index) => {
    let data = rawdata.fields;

    function ceilRate(number) {
      return Math.ceil(number * 100) / 100;
    };

    let winRate = ceilRate(data.champ_middle_data_win);
    let pickRate = ceilRate(data.champ_middle_data_pick);
    let banRate = ceilRate(data.champ_middle_data_ban);

    win_calc_list.push(winRate);
    pick_calc_list.push(pickRate);
    ban_calc_list.push(banRate);

    data.champ_middle_data_win = winRate;
    data.champ_middle_data_pick = pickRate;
    data.champ_middle_data_ban = banRate;
    });
  };

  push_rate_list();

  let calc_champ_rate = {}

  function calc_rate_list(win, pick, ban, rank){
    let sum = 0;
    let i = 0;
    let sort_dict = {};

    win.map((data, index) => {
      calc_champ_rate[index] = 0;
      let score = data * 50;
      calc_champ_rate[index] += score;
      sum += score;
      i += 1;
    });

    pick.map((data, index) => {
      let score = data * 20;
      calc_champ_rate[index] += score;
      sum += score;
    });
    ban.map((data, index) => {
      let score = data * 20;
      calc_champ_rate[index] += score;
      sum += score;
    });

    let avg = sum / i

    var sortable = [];
    for (var name in calc_champ_rate){
      sortable.push([name, calc_champ_rate[name]]);
    }

    sortable.sort(function(a, b) {
      return b[1] - a[1];
    });

    for (var data in sortable){
      sort_dict[sortable[data][0]] = sortable[data][1];
    };

    return [sort_dict, avg];
  };

  let calc_rate_data = calc_rate_list(win_calc_list, pick_calc_list, ban_calc_list, rank)

  function plus_weight(rank) {
    rank.map((rawdata, index)=>{
      let data = rawdata.fields;
      data['weight'] = calc_rate_data[0][index];
    });

    rank.sort((a, b) => b.fields.weight - a.fields.weight);

    return rank;
  };
  
  let re_rank = plus_weight(rank);

  let i = 0;
  let list = re_rank.map((rawdata, index) => {
    let data = rawdata.fields;
    let weight = parseInt(data.weight);
    let avg = parseInt(calc_rate_data[1]);
    let ver = data.champ_middle_data_version;
    let winRate = data.champ_middle_data_win;
    let pickRate = data.champ_middle_data_pick;
    let banRate = data.champ_middle_data_ban;

    function getId(data) {
      let id_split = data.split('.')
      let id = id_split[0]
      return id;
    };

    function getImg(ver, img) {
      let image = "https://ddragon.leagueoflegends.com/cdn/" + ver + "/img/champion/" + img;
      return image;
    };

    // 조건에 해당하는 애들만 ui 에 띄우기
    let uiCondition = 0.3
    if (winRate != 0){
      if (pickRate > uiCondition){
        i += 1;
      };
    };

    let ranking = "1";
    if (weight >= avg * 1.3) {
      ranking = "0";
    } else if (weight >= avg * 1.2 && weight < avg * 1.3) {
      ranking = "1";
    } else if (weight >= avg * 1.1 && weight < avg * 1.2) {
      ranking = "2";
    } else if (weight >= avg * 1.0 && weight < avg * 1.1) {
      ranking = "3";
    } else if (weight >= avg * 0.9 && weight < avg * 1.0) {
      ranking = "4";
    } else if (weight >= avg * 0.1 && weight < avg * 0.9) {
      ranking = "5";
    }

    // 해야할 일 data를 나름의 기준을 세워서 순위를 정한 후 보여줘야함
    // 데이터를 들고올 때 너무 느린데 해결 방법을 찾아야할 듯
    // -> 이거는 통계를 db에 넣고 직접 들고오기로 함.

    let championImg = getImg(ver, data.champ_middle_data_img);

    let champId = getId(data.champ_middle_data_img);


    // 승률이 0퍼가 아닌 챔피언들만 보여줌.
    return (
      <>
        { winRate !== 0 ?
          pickRate >= uiCondition ? (<styled.RankingDataWrapBox key={index}>
            <styled.RankingDataBox $width="10%">{i}</styled.RankingDataBox>
            <styled.RankingDataBox $width="30%">
              <styled.RankingChampionLink $size="20%" to={`/champions/${champId}`}>
                <styled.ChampionsImgStyle $size="24px" src={championImg} />
              </styled.RankingChampionLink>
              <styled.RankingChampionLink $size="80%" to={`/champions/${champId}`}>
                  <styled.RankingChampionNameBox>{data.champ_middle_data_name}</styled.RankingChampionNameBox>
              </styled.RankingChampionLink>
            </styled.RankingDataBox>
            <styled.RankingDataBox $width="10%">{ranking === "0" ? "OP" : ranking}</styled.RankingDataBox>
            {/* <styled.RankingDataBox $width="10%">{ranking}</styled.RankingDataBox> */}
            <styled.RankingDataBox $width="10%">{winRate + "%"}</styled.RankingDataBox>
            <styled.RankingDataBox $width="10%">{pickRate + "%"}</styled.RankingDataBox>
            <styled.RankingDataBox $width="10%">{banRate + "%"}</styled.RankingDataBox>
            <styled.RankingDataBox $width="20%">
              {data.champ_middle_data_counter1.name !== "N/A" ? 
              (<styled.RankingChampionLink $size="auto" to={`/champions/${getId(data.champ_middle_data_counter1.img)}`}>
                <styled.CounterImgStyle src={getImg(ver, data.champ_middle_data_counter1.img)} />
              </styled.RankingChampionLink>) : <></>}
              {data.champ_middle_data_counter2.name !== "N/A" ? 
              (<styled.RankingChampionLink $size="auto" to={`/champions/${getId(ver, data.champ_middle_data_counter2.img)}`}>
                <styled.CounterImgStyle src={getImg(ver, data.champ_middle_data_counter2.img)} />
              </styled.RankingChampionLink>) : <></>}
              {data.champ_middle_data_counter3.name !== "N/A" ? 
              (<styled.RankingChampionLink $size="auto" to={`/champions/${getId(ver, data.champ_middle_data_counter3.img)}`}>
                <styled.CounterImgStyle src={getImg(ver, data.champ_middle_data_counter3.img)} />
              </styled.RankingChampionLink>) : <></>}
            </styled.RankingDataBox>
          </styled.RankingDataWrapBox>) : <></>
           :
          <></>
      }
      </>
    )
  });

  return (
    <>
      <NavTitle />
      {list}
    </>
  )
}

export function MiddleLineButton() {
  return (
    <>
      <styled.ChampionsBox $height="50px">
        <styled.WrappingBox>
          <OptionTierButton />
          <OptionVersionButton />
        </styled.WrappingBox>
        <styled.WrappingBox>
          <LineButton />
        </styled.WrappingBox>
      </styled.ChampionsBox>
    </>
  );
}