import React, { useEffect } from "react";
import { useDispatch } from 'react-redux';
import { useLocation, useNavigate } from 'react-router-dom';
import Nav from "view/nav";
import TopBox from "./boxes/topBox";
import { BlankDiv, ContainerDiv } from "./searchStyle/topBoxStyle";
import Button from "./boxes/refreshButton"
import GetSearchData from "./dataHandling/api/getSearchData";
import BottomBox from "./boxes/bottomBox";
import { fetchDataRequest, fetchDataSuccess, fetchDataFailure } from "redux/dataSlice";

function SearchPage() {
  const dispatch = useDispatch();
  let location = useLocation();
  let navigate = useNavigate();
  let gameName = "";

  useEffect(() => {
    const nickname = location.state.nickname;
    fetchDataRequest();
    if (gameName) {
      fetch(`http://localhost:8000/search/${gameName}/`)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          dispatch(data);
        });
    } else {
      fetch('http://localhost:8000/search/Hide%20on%20bush')
        .then(response => response.json())
        // .then(data => setItems(data));
    }
    // GetSearchData()
    //   .then((res) => {
    //     dispatch(fetchDataSuccess(res));
    //   // }).catch((err) => {
    //   //   dispatch(fetchDataFailure(err));
    //   //   navigate('/');
    //   //   setTimeout(() => {
    //   //     alert('정확한 소환사 이름을 입력해주세요');
    //   //   }, 500);
    //   });
  }, [dispatch]);

  return (
    <div>
      {/* <Nav></Nav> */}
      {/* <ContainerDiv>
        <TopBox />
        <Button />
        <BlankDiv />
        <BottomBox />
      </ContainerDiv>
      <BlankDiv /> */}
    </div>
  );
}

export default SearchPage;