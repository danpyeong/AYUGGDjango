import { Link, useLocation } from "react-router-dom";
import * as styled from "../nav/navStyle";
import { useNavigate } from 'react-router-dom';
import { useState } from "react";

function Nav() {
  let navigate = useNavigate();
  const [inputText, setInputText] = useState('');
  const location = useLocation();

  const searchButtonClick = () => {
    const [gameName, tagLine] = inputText.split('#');
    if (gameName && tagLine) {
      navigate(`/search/${gameName}/${tagLine}`);
    } else {
      alert('정확히 입력해주세요!!');
    }
  }
  const activeEnter = (e) => {
    if(e.key === "Enter") {
      searchButtonClick();
    }
  }

  return (
    <styled.NavBox>
      <styled.NavBoxButton>
        <Link to="/">
          <styled.Logo src={'/assets/images/logo/navbar-logo.png'} />
        </Link>
        <LinkList url="/" name="홈" />
        <LinkList url="/champions" name="챔피언분석" />
        <LinkList url="/statistics" name="통계" />
        <LinkList url="/ranking" name="랭킹" />
        <LinkList url="/multi" name="멀티서치" />
      </styled.NavBoxButton>
      <styled.NavBoxSearch>
        <styled.Search>
          <styled.SearchSelect>
            <option value="KR">KR</option>
          </styled.SearchSelect>
          <styled.SearchInput value={inputText} onChange={(e) => { setInputText(e.target.value); }} onKeyDown={activeEnter}/>
          <styled.SearchButton onClick={searchButtonClick} >
            <styled.SearchIcon src={`${process.env.PUBLIC_URL}` + '/assets/images/search-icon/search-icon-24.svg'} />
          </styled.SearchButton>
        </styled.Search>
      </styled.NavBoxSearch>
    </styled.NavBox>
  );
}

function LinkList(props) {
  const { pathname } = useLocation();
  let width;
  const pathName = pathname.split('/')[1]
  const url = props.url.split('/')[1]

  switch (props.name) {
    case '홈':
      width = "20px";
      break;
    case '통계':
      width = "40px";
      break;
    case '랭킹':
      width = "40px";
      break;
    case '멀티서치':
      width = "80px";
      break;
    case '챔피언분석':
      width = "100px";
      break;
  }

  return (
    <>
      <styled.ListBox $width={width} $pathname={pathName} $url={url}>
        <styled.ListStyle to={props.url} $pathname={pathName} $url={url}>{props.name}</styled.ListStyle>
      </styled.ListBox>
    </>
  );
}

export default Nav;
