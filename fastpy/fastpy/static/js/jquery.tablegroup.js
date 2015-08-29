/*
 * jQuery tableGroup plugin
 * Version: 0.1.0
 *
 * Copyright (c) 2007 Roman Weich
 * http://p.sohei.org
 *
 * Dual licensed under the MIT and GPL licenses 
 * (This means that you can choose the license that best suits your project, and use it accordingly):
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Changelog: 
 * v 0.1.0 - 2007-05-20
 */

(function($) 
{
	var defaults = {
		groupColumn : 1,
		useNumChars : 0,
		groupClass : ''
	};

	/**
	 * Returns the cell element which has the passed column index value.
	 * @param {element} table	The table element.
	 * @param {array} cells		The cells to loop through.
	 * @param {integer} col	The column index to look for.
	 */
	var getCell = function(table, cells, col)
	{
		for ( var i = 0; i < cells.length; i++ )
		{
			if ( cells[i].realIndex === undefined ) //the test is here, because rows/cells could get added after the first run
			{
				fixCellIndexes(table);
			}
			if ( cells[i].realIndex == col )
			{
				return cells[i];
			}
		}
		return null;
	};

	/**
	 * Calculates the actual cellIndex value of all cells in the table and stores it in the realCell property of each cell.
	 * Thats done because the cellIndex value isn't correct when colspans or rowspans are used.
	 * Originally created by Matt Kruse for his table library - Big Thanks! (see http://www.javascripttoolbox.com/)
	 * @param {element} table	The table element.
	 */
	var fixCellIndexes = function(table) 
	{
		var rows = table.rows;
		var len = rows.length;
		var matrix = [];
		var cols = 0;
		for ( var i = 0; i < len; i++ )
		{
			var cells = rows[i].cells;
			var clen = cells.length;
			cols = Math.max(clen, cols);
			for ( var j = 0; j < clen; j++ )
			{
				var c = cells[j];
				var rowSpan = c.rowSpan || 1;
				var colSpan = c.colSpan || 1;
				var firstAvailCol = -1;
				if ( !matrix[i] )
				{ 
					matrix[i] = []; 
				}
				var m = matrix[i];
				// Find first available column in the first row
				while ( m[++firstAvailCol] ) {}
				c.realIndex = firstAvailCol;
				for ( var k = i; k < i + rowSpan; k++ )
				{
					if ( !matrix[k] )
					{ 
						matrix[k] = []; 
					}
					var matrixrow = matrix[k];
					for ( var l = firstAvailCol; l < firstAvailCol + colSpan; l++ )
					{
						matrixrow[l] = 1;
					}
				}
			}
		}
		table.numCols = cols;
	};
	
	/**
	 * Simple grouping of rows in a table.
	 *
	 * @param {map} options			An object for optional settings (options described below).
	 *
	 * @option {integer} groupColumn		The column to group after.
	*							Index starting at 1!
	 *							Default value: 1
	 * @option {string} groupClass		A CSS class that is set on the inserted grouping row.
	 *							Default value: ''
	 * @option {integer} useNumChars		Defines the number of characters that are used to group the rows together. Set it to 0 to use all characters.
	 *							Default value: 0
	 *
	 * @example $('#table').tableGroup();
	 * @desc Group the rows using the default settings.
	 *
	 * @example $('#table').tableGroup({groupColumn: 3, groupClass: 'mygroups', useNumChars: 1});
	 * @desc Group the rows after the first character in the third column. Set the CSS class "mygroups" to all inserted rows.
	 *
	 * @type jQuery
	 *
	 * @name tableGroup
	 * @cat Plugins/tableGroup
	 * @author Roman Weich (http://p.sohei.org)
	 */
	$.fn.tableGroup = function(options)
	{
		var settings = $.extend({}, defaults, options);

        return this.each(function()
        {
			var tboI, rowI, gC, body, row, $row, lastIH, c, cStr, match, tc;
			var itemCount =0;
			gC = settings.groupColumn - 1;
			lastIH = null;
			if ( !this.tBodies || !this.tBodies.length )
			{
				return;
			}
			cStr = 'tGroup ' + settings.groupClass;
			//loop through the bodies
			for ( tboI = 0; tboI < this.tBodies.length; tboI++ )
			{
				body = this.tBodies[tboI];
				//loop through the rows
				for ( rowI = 0; rowI < body.rows.length; rowI++ )
				{
					row = body.rows[rowI];
					c = getCell(this, row.cells, gC);
					if ( c )
					{
						if ( settings.useNumChars == 0 )
						{
							match = c.innerHTML;
						}
						else
						{
							tc = c.textContent || c.innerText;
							match = tc.substr(0, settings.useNumChars);
						}
						if ( match !== lastIH )
						{
							if($row){
								$row.find('td')[0].innerHTML += ' <span class="item-count">(<em>'+itemCount+'</em>)</span>';
							}
							itemCount = 0;
							var groupName = match;
							if(groupName==''){groupName='(Empty)';}
							//insert grouping row
							$row = $('<tr class="' + cStr + '"><td colspan="' + this.numCols + '">' + groupName + '</td></tr>');
							$row.find('td')[0].realIndex = 0;
							$(row).before($row);
							lastIH = match;
						}else{
							itemCount++;
						}
					}
				}
				if($row){
					$row.find('td')[0].innerHTML += ' <span class="item-count">(<em>'+itemCount+'</em>)</span>';
				}
			}
        }); 
	};

	/**
	 * Removes the grouping rows from the table.
	 *
	 * @type jQuery
	 *
	 * @name tableUnGroup
	 * @cat Plugins/tableGroup
	 * @author Roman Weich (http://p.sohei.org)
	 */
	$.fn.tableUnGroup = function()
	{
        return this.each(function()
        {
			$('tr.tGroup', this).remove();
        }); 
	};
})(jQuery);
