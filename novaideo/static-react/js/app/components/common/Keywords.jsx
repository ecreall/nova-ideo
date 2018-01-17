import React from 'react';
import Icon from 'material-ui/Icon';

const styles = {
  icon: {
    color: 'rgb(88, 88, 88)',
    fontSize: 12
  },
  keywordsContainer: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingLeft: 15,
    paddingRight: 5,
    marginBottom: 5
  },
  keywordsText: {
    color: 'rgb(88, 88, 88)',
    marginLeft: 4,
    fontSize: 12
  }
};

const Keywords = ({ keywords, onKeywordClick }) => {
  const onClick = (k) => {
    if (onKeywordClick) {
      onKeywordClick(k);
    }
  };

  return (
    <div style={styles.keywordsContainer}>
      <Icon style={styles.icon} className={'mdi-set mdi-tag-multiple'} />
      {keywords.map((k, index) => {
        return (
          <div
            key={k}
            title={k}
            onClick={() => {
              return onClick(k);
            }}
          >
            <span style={{ ...styles.keywordsText, ...(onKeywordClick ? { cursor: 'pointer' } : {}) }}>
              {k}
              {index + 1 !== keywords.length ? ',' : ''}
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default Keywords;