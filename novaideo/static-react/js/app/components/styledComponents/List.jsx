import glamorous from 'glamorous';
import { ListItem as MuiListItem, ListItemText as MuiListItemText, ListItemIcon as MuiListItemIcon } from 'material-ui/List';

export const ListItem = glamorous(MuiListItem)((props) => {
  return {
    borderRadius: 5,
    padding: '0 16px 0 8px',
    margin: '0 15px',
    width: '100%',
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

export const ListItemText = glamorous(MuiListItemText)((props) => {
  return {
    padding: 0,
    '& .menu-item-text': {
      flex: '1 1 auto',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontSize: 15,
      color: props.color || '#2c2d30'
    }
  };
});

export const ListItemIcon = glamorous(MuiListItemIcon)((props) => {
  return {
    width: 20,
    height: 28,
    marginRight: 10,
    color: props.color || '#a0a0a2'
  };
});