const filterItems = (items: any[], query: string): any[] => {
    let _filteredItems = [];
    for (let i = 0; i < items.length; i++) {
        let item = items[i];

        if (item.name.toLowerCase().indexOf(query.toLowerCase()) === 0) {
            _filteredItems.push(item);
        }
    }
    return _filteredItems;
}

export default filterItems

