import React from 'react';
import Icon from 'material-ui/Icon';

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
    marginLeft: 5,
    marginRight: 5,
    backgroundColor: '#e8e8e8',
    borderRadius: 3
  },
  keywordsText: {
    color: '#a0a0a2',
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