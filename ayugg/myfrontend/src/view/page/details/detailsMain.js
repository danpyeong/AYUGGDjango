import Nav from "../../nav";
import FirstArticle from "./detailsBasicInfo";
import SecondArticle from "./detailsRune";
import ThirdArticle from "./detailsItem";
import { getChampionDetailDataApi as getChamp, getChampionBasicDataApi as getBasicInfo,
  getChampionRanking as getRanking  } from "../../../model/api/champions";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useSelector } from "react-redux";

function ChampionsDetails() {
  const [basicData, setbasicData] = useState();
  const [champData, setchampData] = useState();
  const [rankingData, setRankingData ] = useState(); 
  const { id } = useParams();

  let line = useSelector((state)=>{ return state.rankingLine })
  let tier = useSelector((state)=>{ return state.rankingTier })
  let ver = useSelector((state)=>{ return state.rankingVersion })

  useEffect(()=>{
    getChamp(id).then((raw) =>{
      setchampData(JSON.parse(raw))
    })
    getBasicInfo(id).then((raw)=>{
      setbasicData(JSON.parse(raw))
    })
    getRanking(tier, line, ver)
      .then((data)=>{
        setRankingData(JSON.parse(data));
      })
  },[id, tier, line, ver]);

  return (
    <>
      <Nav />
      <FirstArticle champ={champData} basic={basicData} ranking={rankingData} id={ id } />
      <SecondArticle champ={champData} basic={basicData} ranking={rankingData} id={ id } />
      <ThirdArticle champ={champData} basic={basicData} ranking={rankingData} id={ id } />
    </>
  );
}

export default ChampionsDetails;
