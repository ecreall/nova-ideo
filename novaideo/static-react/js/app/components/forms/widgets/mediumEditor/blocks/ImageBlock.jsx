import React from 'react';

import { EditorBlock } from 'draft-js';

import BlockDataManager from '../BlockDataManager';

export const DumbImageBlock = (props) => {
  const { blockProps, block } = props;
  const data = block.getData();
  const src = data.get('src');
  const position = data.get('position');
  const size = data.get('size');
  if (src !== null) {
    return (
      <BlockDataManager
        {...props}
        readOnly={blockProps.readOnly}
        data={{ src: src, position: position, size: size }}
        className="md-block-with-data"
      >
        <div className="md-block-image-inner-container">
          <img alt={block.text} src={src} />
        </div>
        <figcaption>
          <EditorBlock {...props} />
        </figcaption>
      </BlockDataManager>
    );
  }
  return <EditorBlock {...props} />;
};

export default DumbImageBlock;