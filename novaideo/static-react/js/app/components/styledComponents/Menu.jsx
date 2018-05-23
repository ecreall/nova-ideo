import glamorous from 'glamorous';
import MuiMenuItem from '@material-ui/core/MenuItem';
import MuiMenuList from '@material-ui/core/MenuList';

export const MenuList = glamorous(MuiMenuList)({
  paddingTop: 15,
  paddingBottom: 15,
  minWidth: 230
});

export const MenuItem = glamorous(MuiMenuItem)((props) => {
  return {
    borderRadius: 5,
    padding: '0 16px 0 8px',
    margin: '0 15px',
    minHeight: 28,
    transition: 'none',
    '&:hover, &:focus, &:active': {
      backgroundColor: props.hoverColor,
      '& .menu-item-icon': {
        color: 'white'
      },
      '& .menu-item-text': {
        color: 'white',
        textShadow: '0 1px 0 rgba(0,0,0,.1)'
      }
    }
  };
});