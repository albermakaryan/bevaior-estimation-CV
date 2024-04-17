def collate_fn(batch):
    
    """
    This function is used to collate the batch of data.
    
    Parameters
    ----------
    batch : list
        List of input data.
        
    Returns
    -------
    tuple
        Tuple of input data.
    """
    return tuple(zip(*batch))