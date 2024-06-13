import { useEffect, useState } from "react";
import * as styled from "./champsStyle";
// import { ChampionDataApi } from "model/api/champions";
import { ChampionDataApi } from "../../../model/api/champions";

const champServerData = await ChampionDataApi();

export function Input() {
  const [data, setData] = useState();
  useEffect(() => {
    setData(champServerData);
  }, []);

  return (
    data && <InputData data={data} />
  )
}

function InputData(props){
  const imgData = props.data;
  const [userInputK, setUserInputK] = useState("");
  const [userInputE, setUserInputE] = useState();
  // let navigate = useNavigate();

  const onChangeInput = e => {
    setUserInputK(e.target.value.toLowerCase());
    setUserInputE(e.target.value === "" ? null : e.target.value.toLowerCase());
  };
  const onReset = () => {
    setUserInputK("");
  };
  const handleOnClick = () => {
    // navigate('/');
  };
  const handleOnKeyPress = e => {
    if (e.key === 'Enter') {
      handleOnClick();
    }
  };

  // 한글 이름으로 검색 시
  const searchedK = imgData.filter((item) =>
    item.champion_name.toLowerCase().includes(userInputK)
  );

  // 영문 이름으로 검색 시
  const searchedE = imgData.filter((item) =>
    item.champion_id.toLowerCase().includes(userInputE)
  );

  return (
    <>
      <styled.ChampionsInputBox>
        <styled.ChampionsInput
          type="text"
          value={userInputK}
          placeholder="챔피언 검색 (가렌, 갱플랭크 ...)"
          onChange={onChangeInput}
          onKeyDown={handleOnKeyPress}
        />
        <styled.ResetButton onClick={onReset}>X</styled.ResetButton>
      </styled.ChampionsInputBox>
      <styled.ChampionsOlStyle>
        {searchedK.map((item) => (
          <ChampionsImgFull key={item.champion_id} {...item} />
        ))}
        {searchedE.map((item) => (
          <ChampionsImgFull key={item.champion_id} {...item} />
        ))}
      </styled.ChampionsOlStyle>
    </>
  );
}

export function ChampionsImgFull({ champion_id, champion_name, champion_img, champion_version }){
  let startUrl = "https://ddragon.leagueoflegends.com/cdn/"
  let middleUrl = "/img/champion/"
  let src = startUrl + champion_version + middleUrl + champion_img
  
  let listData = (
    <styled.ListBox key={champion_id}>
      <li>
        <styled.ChampionLink to={`/champions/${champion_id}`}>
          <styled.ChampionsImgStyle $size="48px" src={src} />
        </styled.ChampionLink>
        <styled.ChampionLink to={`/champions/${champion_id}`}>
          <styled.ChampionsSpanStyle>{champion_name}</styled.ChampionsSpanStyle>
        </styled.ChampionLink>
      </li>
    </styled.ListBox>
  )
  
  return  <>{listData}</>
}