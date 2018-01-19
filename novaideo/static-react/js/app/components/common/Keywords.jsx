import React from 'react';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';

const styles = {
  icon: {
    color: '#a0a0a2',
    fontSize: 12
  },
  keywordsContainer: {
    display: 'flex',
    alignItems: 'center',
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingLeft: 5,
    paddingRight: 5,
    marginBottom: 2,
    marginLeft: 7,
    marginRight: 3,
    backgroundColor: '#e8e8e8',
    borderRadius: 3
  },
  keywordsText: {
    color: '#a0a0a2',
    marginLeft: 4,
    fontSize: 12
  },
  active: {
    cursor: 'pointer'
  }
};

const Keywords = ({ keywords, onKeywordClick, classes }) => {
  const onClick = (k) => {
    if (onKeywordClick) {
      onKeywordClick(k);
    }
  };

  return (
    <div className={classes.keywordsContainer}>
      <Icon className={classNames(classes.icon, 'mdi-set mdi-tag-multiple')} />
      {keywords.map((k, index) => {
        return (
          <div
            key={k}
            title={k}
            onClick={() => {
              return onClick(k);
            }}
          >
            <span className={classNames(classes.keywordsText, { [classes.active]: onKeywordClick })}>
              {k}
              {index + 1 !== keywords.length ? ',' : ''}
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default withStyles(styles)(Keywords);